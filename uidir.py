# coding: utf-8

import console,os,ui

class MyTableViewDataSource (object):
   # sel = [None]

    def __init__(self,setter, base_dir = '.'):
        self.dir = base_dir
        self.setter = setter
        _, folders, files = next(os.walk(base_dir))
        folders.insert(0,'..')
        self.data = (folders,files)
        self.sel = [None]
    def tableview_number_of_sections(self, tableview):
        return 2

    def tableview_number_of_rows(self, tableview, section):
        return len(self.data[section])

    def tableview_cell_for_row(self, tableview, section, row):
        cell = ui.TableViewCell()
        cell.accessory_type = ('disclosure_indicator', 'detail_button')[section]
        cell.text_label.text = self.data[section][row]
        return cell

    def tableview_title_for_header(self, tableview, section):
        return ('Folders','Files')[section]

    def tableview_did_select(self, tableview, section, row):
        '@type tableview: ui.TableView'
        if section == 0:
            dir = os.path.join(self.dir, self.data[section][row])
            if os.path.exists(dir):
                self.dir = dir
            newv = FileViewer(self.setter,self.dir)
            nav = tableview.superview.navigation_view
            nav.push_view(newv)
        else:
           # print self.dir, self.data[section][row]
            self.sel[0] = os.path.join(self.dir, self.data[section][row])
            tableview.superview.navigation_view.close()
            self.setter(self.sel[0])

    def tableview_accessory_button_tapped(self, tableview, section, row):
        full = os.path.join(self.dir,self.data[section][row])
        stats =  os.stat(full)
        console.hud_alert('Size: {0} KB'.format(stats.st_size//1024))

class FileViewer(ui.View):
    def __init__(self,setter, base_dir = '.', *args, **kargs):
        table = ui.TableView(*args, **kargs)
        table.name = 'FileTable'
        self.src = MyTableViewDataSource(setter, base_dir)
        table.data_source = table.delegate = self.src
        table.flex = 'WHTBLR'
        #self.view = ui.View(name = base_dir)
        self.background_color = 'white'
        self.add_subview(table)

    @property
    def selection(self):
        return self.src.sel[0]

def getFile(setter):
    fv = FileViewer(setter)
    nv = ui.NavigationView(fv)
    nv.name = 'File Selector'
    nv.present('popover')
    ui.in_background(nv.wait_modal)
    nv.wait_modal()
   # return fv.selection

import ed  # if this script in run then launch the editor
