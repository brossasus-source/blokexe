import sys,os,re,time,base64,random,threading,webbrowser
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
app=QApplication(sys.argv)
W={}
VERSION="1.0.0"
VARS={}
def G(w):
    if isinstance(w,QLineEdit): return w.text()
    if isinstance(w,QTextEdit): return w.toPlainText()
    if isinstance(w,(QCheckBox,QRadioButton)): return "1" if w.isChecked() else "0"
    if isinstance(w,QComboBox): return w.currentText()
    if isinstance(w,QListWidget):
        i=w.currentItem(); return i.text() if i else ""
    if isinstance(w,(QSpinBox,QSlider,QProgressBar)): return str(w.value())
    if isinstance(w,QDateEdit): return w.date().toString("dd.MM.yyyy")
    if isinstance(w,(QSystemTrayIcon,QMenuBar)): return w.sel
    if isinstance(w,QCalendarWidget): return w.selectedDate().toString("dd.MM.yyyy")
    return w.text() if hasattr(w,"text") else ""
def SET(n,v):
    w=W[n]
    if isinstance(w,QLineEdit): w.setText(v)
    elif isinstance(w,QTextEdit): w.setPlainText(v)
    elif isinstance(w,(QCheckBox,QRadioButton)): w.setChecked(v.lower() in ("1","true","evet"))
    elif isinstance(w,QComboBox): w.setCurrentText(v)
    elif isinstance(w,(QSpinBox,QSlider,QProgressBar)): w.setValue(int(float(v or 0)))
    elif hasattr(w,"setText"): w.setText(v)
def V(s):
    def r(m):
        n=m.group(1)
        if n=="tarih": return time.strftime("%d.%m.%Y")
        if n=="saat": return time.strftime("%H:%M:%S")
        if n=="surum": return VERSION
        if n=="masaustu": return QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)
        if n in VARS: return str(VARS[n])
        return G(W[n]) if n in W else m.group(0)
    return re.sub(r"\{(\w+)\}",r,s)
def CMP(a,op,b):
    try: x,y=float(a),float(b)
    except Exception: x,y=a,b
    if op=="içerir": return str(b) in str(a)
    return {"=":x==y,"≠":x!=y,">":x>y,"<":x<y,"≥":x>=y,"≤":x<=y}.get(op,False)
def CALC(e):
    e=e.strip() or "0"
    if re.fullmatch(r"[0-9+\-*/(). %]+",e):
        try:
            r=eval(e,{"__builtins__":{}},{}); return str(int(r)) if float(r).is_integer() else str(round(r,6))
        except Exception: return "0"
    return "0"
def PICK(n,k):
    r=QFileDialog.getOpenFileName(root,"Dosya seç")[0] if k=="open" else QFileDialog.getSaveFileName(root,"Kaydet")[0] if k=="save" else QFileDialog.getExistingDirectory(root,"Klasör seç")
    if r: SET(n,r)
def ASK(n,t):
    r,ok=QInputDialog.getText(root,root.windowTitle(),V(t))
    if ok: SET(n,r)
def PLY(w): return getattr(w,"p",w)
def STYLE(w,k,v):
    d=getattr(w,"_st",None)
    if d is None: d=w._st={}
    d[k]=v; w.setStyleSheet(";".join(a+":"+b for a,b in d.items()))
def QUIT():
    root.quit=True; root.close()
def MEDIA(s):
    s=V(s).strip()
    return QUrl(s) if s.lower().startswith(("http://","https://")) else QUrl.fromLocalFile(os.path.expandvars(os.path.expanduser(s)))
def MAPURL(s):
    p=[x.strip() for x in V(s).split(",")]
    z=p[2] if len(p)>2 else "15"
    return "https://www.openstreetmap.org/?mlat=%s&mlon=%s#map=%s/%s/%s"%(p[0],p[1],z,p[0],p[1])
root=QWidget();root.setObjectName("root");root.setAttribute(Qt.WA_StyledBackground,True);root.setWindowTitle("Uygulamam");root.resize(600,400)
root.setStyleSheet("QWidget#root{background:#f0f0f0}")
o=QLabel("Etiket",root)
o.setGeometry(275.56671142578125,136.1666717529297,120,24)
W["lbl1"]=o
root.show()
sys.exit(app.exec())
