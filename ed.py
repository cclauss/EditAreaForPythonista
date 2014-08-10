# coding: utf-8
# ed  a proof of concept of using a javascript editor inside a webview
#  uses codemirror to provide a capable editor
#  lightly wrapped in a webview
#
import json,os,ui,uidir

def edopen(sender):
    '''open the file named in the textbox, load into editor'''
    w=sender.superview['webview1']
    f=sender.superview['filename']
    try:
        with open(f.text) as file:
            fmt = 'editAreaLoader.setValue("code",{});'
            w.eval_js(fmt.format(json.dumps(file.read())))
    except (IOError):
        print 'file "{}" not found'.format(f.text)

def edsave(sender):
    '''save the editor content to file in filename textbox'''
    w=sender.superview['webview1']
    f=sender.superview['filename']
    try:
        with open(f.text,'w') as file:
            file.write(w.eval_js('editAreaLoader.getValue("code");'))
    except(IOError):
        print('could not save file "{}"'.format(f.text))

def edselect(sender):
    f=sender.superview['filename']
    def setter(s):
        f.text=s
    uidir.getFile(setter)

#main script

e=ui.load_view('ed')
e['filename'].autocapitalization_type=ui.AUTOCAPITALIZE_NONE
e['filename'].autocorrection_type=False
#srcname='ed.html'  #doesnt work in webview?.  but does in webbrowser...wth?
#srcname='editarea.html'
#print os.path.abspath(srcname)
e['webview1'].load_url(os.path.abspath('editarea.html'))

e.present('panel')
