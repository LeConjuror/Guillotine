from pathlib import Path
from tkinter import Tk, Canvas, Entry, Checkbutton, Text, Button, PhotoImage, filedialog, END, IntVar, StringVar, Scrollbar, LEFT, RIGHT, BOTH, X, Y
from tktooltip import ToolTip
import subprocess
import threading
import sys
import os

if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))
__file__ = application_path

OUTPUT_PATH = Path(__file__).resolve().parent
CONFIG_PATH = OUTPUT_PATH / Path("scalpel.conf")


# UI 
# Canvas Frame
window = Tk()
window.title('Guillotine')
window.geometry("670x720")
window.configure(bg = "#393939")

canvas = Canvas(
    window,
    bg = "#393939",
    height = 720,
    width = 670,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
canvas.place(x = 0, y = 0)

# Input box BG + Title
canvas.create_rectangle(
    40.0,
    30.0,
    630.0,
    80.0,
    fill="#D9D9D9",
    outline="")

canvas.create_text(
    50.0,
    35.0,
    anchor="nw",
    text="Input File",
    fill="#454545",
    font=("Inter Bold", 14 * -1)
)

# Output box BG + Title
canvas.create_rectangle(
    40.0,
    100.0,
    630.0,
    150.0,
    fill="#D9D9D9",
    outline="")

canvas.create_text(
    50.0,
    105.0,
    anchor="nw",
    text="Output Directory",
    fill="#454545",
    font=("Inter Bold", 14 * -1)
)

# Input & Output Input Field
inputBox = Entry()
outputBox = Entry()

for box in [inputBox, outputBox]:
    box.config(
        bd=0,
        highlightthickness=0,
        bg="#D9D9D9",
        fg="#000000"
    )

def browseFile():
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File")
    inputBox.delete(0, END)
    inputBox.insert(0, filename)

def browseDirectory():
    directory = filedialog.askdirectory(initialdir = "/",
                                          title = "Select a Directory")
    outputBox.delete(0, END)
    outputBox.insert(0, directory)

inputBox.place (x=50.0, y=50.0,  width=480, height=25)
outputBox.place(x=50.0, y=120.0, width=480, height=25)

# Input & Output Browse Buttons

browseInButton  = Button(command=browseFile)
browseOutButton = Button(command=browseDirectory)

for button in [browseInButton, browseOutButton]:
    button.config(
        bd=0,
        highlightthickness=0,
        bg="#999999", 
        activebackground="#666666",
        fg="#222222", 
        activeforeground="#111111",
        font=("Inter Bold", 14 * -1),
        text="Browse",
        relief="groove"
    )

browseInButton.place(x=530.0, y=40.0, width=80.0, height=30.0)
browseOutButton.place(x=530.0, y=110.0, width=80.0, height=30.0)

# Advanced Options

canvas.create_text(
    40.0,
    170.0,
    anchor="nw",
    text="Advanced Options:",
    fill="#FFFFFF",
    font=("Inter Bold", 15 * -1)
)


OPTION_B = IntVar()
OPTION_D = IntVar()
OPTION_E = IntVar()
OPTION_N = IntVar()
OPTION_O = IntVar()
OPTION_Q = IntVar()
OPTION_P = IntVar()
OPTION_R = IntVar()

bButton = Checkbutton(canvas, variable=OPTION_B, text="Loose Carving")
dButton = Checkbutton(canvas, variable=OPTION_D, text="Generate DB")
eButton = Checkbutton(canvas, variable=OPTION_E, text="Nested Match")
rButton = Checkbutton(canvas, variable=OPTION_R, text="First Match Only")
oButton = Checkbutton(canvas, variable=OPTION_O, text="No Subdir")
nButton = Checkbutton(canvas, variable=OPTION_N, text="No Extensions")
pButton = Checkbutton(canvas, variable=OPTION_P, text="Preview Mode")
qButton = Checkbutton(canvas, variable=OPTION_Q, text="Cluster Aligned")
qEntry = Entry()
qEntry.config(
        bd=0,
        highlightthickness=0,
        bg="#D9D9D9",
        fg="#000000",
        font=("Inter", 15 * -1)
    )
qEntry.place(x=590.0, y=230.0,  width=50, height=20)

OPTION_BUTTONS = [bButton, dButton, eButton, nButton, oButton, qButton, pButton, rButton]

tooltips = {
    bButton: "Carve files even if defined footers aren't discovered within maximum carve size for file type.",
    dButton: "Generate header/footer database; will bypass certain optimizations and discover all footers, so performance suffers. Doesn't affect the set of files carved.",
    eButton: "Do nested header/footer matching, to deal with structured files that may contain embedded files of the same type.  Applicable only to FORWARD / NEXT patterns.",
    rButton: "Find only first of overlapping headers/footers.",
    oButton: "Don't organize carved files by type. Default is to organize carved files into subdirectories.",
    nButton: "Don't add extensions to extracted files.",
    pButton: "Perform image file preview; audit log indicates which files would have been carved, but no files are actually carved.  Useful for indexing file or data fragment locations or supporting in-place file carving.",
    qButton: "Carve only when header is cluster-aligned. (Needs Cluster Size Input)"
}

for button in OPTION_BUTTONS:
    button.config(bd=0,
                  highlightthickness=0,
                  selectcolor = "#555555",
                  bg="#393939", 
                  activebackground="#393939",
                  fg="#FFFFFF", 
                  activeforeground="#AAAAAA",
                  font=("Inter", 15 * -1))
    ToolTip(button, msg=tooltips[button], delay=0.5) 

bButton.place(x=30.0, y=200.0)
dButton.place(x=170.0,y=200.0)
eButton.place(x=310.0,y=200.0)
rButton.place(x=450.0,y=200.0)
oButton.place(x=30.0, y=230.0)
nButton.place(x=170.0,y=230.0)
pButton.place(x=310.0,y=230.0)
qButton.place(x=450.0,y=230.0)

# File Types

canvas.create_text(
    40.0,
    270.0,
    anchor="nw",
    text="File Types:",
    fill="#FFFFFF",
    font=("Inter Bold", 15 * -1)
)

OPTION_art = IntVar()
OPTION_bmp = IntVar()
OPTION_gif = IntVar()
OPTION_jpg = IntVar()
OPTION_png = IntVar()
OPTION_tif = IntVar()
OPTION_avi = IntVar()
OPTION_asf = IntVar()
OPTION_fws = IntVar()
OPTION_mov = IntVar()
OPTION_mpg = IntVar()
OPTION_wmv = IntVar()
OPTION_mp3 = IntVar()
OPTION_raa = IntVar()
OPTION_wav = IntVar()
OPTION_wma = IntVar()
OPTION_dat = IntVar()
OPTION_doc = IntVar()
OPTION_htm = IntVar()
OPTION_jav = IntVar()
OPTION_pdf = IntVar()
OPTION_wpc = IntVar()
OPTION_sez = IntVar()
OPTION_rar = IntVar()
OPTION_tgz = IntVar()
OPTION_zip = IntVar()
OPTION_rpm = IntVar()
OPTION_ema = IntVar()
OPTION_dbx = IntVar()
OPTION_idx = IntVar()
OPTION_mbx = IntVar()
OPTION_ost = IntVar()
OPTION_pst = IntVar()

artButton = Checkbutton(canvas, variable=OPTION_art, text="art")
bmpButton = Checkbutton(canvas, variable=OPTION_bmp, text="bmp")
gifButton = Checkbutton(canvas, variable=OPTION_gif, text="gif")
jpgButton = Checkbutton(canvas, variable=OPTION_jpg, text="jpg")
pngButton = Checkbutton(canvas, variable=OPTION_png, text="png")
tifButton = Checkbutton(canvas, variable=OPTION_tif, text="tif")
aviButton = Checkbutton(canvas, variable=OPTION_avi, text="avi")
asfButton = Checkbutton(canvas, variable=OPTION_asf, text="asf")
fwsButton = Checkbutton(canvas, variable=OPTION_fws, text="fws")
movButton = Checkbutton(canvas, variable=OPTION_mov, text="mov")
mpgButton = Checkbutton(canvas, variable=OPTION_mpg, text="mpg")
wmvButton = Checkbutton(canvas, variable=OPTION_wmv, text="wmv")
mp3Button = Checkbutton(canvas, variable=OPTION_mp3, text="mp3")
raaButton = Checkbutton(canvas, variable=OPTION_raa, text="ra")
wavButton = Checkbutton(canvas, variable=OPTION_wav, text="wav")
wmaButton = Checkbutton(canvas, variable=OPTION_wma, text="wma")
datButton = Checkbutton(canvas, variable=OPTION_dat, text="dat")
docButton = Checkbutton(canvas, variable=OPTION_doc, text="doc")
htmButton = Checkbutton(canvas, variable=OPTION_htm, text="htm")
javButton = Checkbutton(canvas, variable=OPTION_jav, text="java")
pdfButton = Checkbutton(canvas, variable=OPTION_pdf, text="pdf")
wpcButton = Checkbutton(canvas, variable=OPTION_wpc, text="wpc")
sezButton = Checkbutton(canvas, variable=OPTION_sez, text="7z")
rarButton = Checkbutton(canvas, variable=OPTION_rar, text="rar")
tgzButton = Checkbutton(canvas, variable=OPTION_tgz, text="tgz")
zipButton = Checkbutton(canvas, variable=OPTION_zip, text="zip")
rpmButton = Checkbutton(canvas, variable=OPTION_rpm, text="rpm")
emaButton = Checkbutton(canvas, variable=OPTION_ema, text="email")
dbxButton = Checkbutton(canvas, variable=OPTION_dbx, text="dbx")
idxButton = Checkbutton(canvas, variable=OPTION_idx, text="idx")
mbxButton = Checkbutton(canvas, variable=OPTION_mbx, text="mbx")
ostButton = Checkbutton(canvas, variable=OPTION_ost, text="ost")
pstButton = Checkbutton(canvas, variable=OPTION_pst, text="pst")

graphButtons = [artButton, bmpButton, gifButton, jpgButton, pngButton, tifButton]
videoButtons = [aviButton, asfButton, fwsButton, movButton, mpgButton, wmvButton ]
audioButtons = [mp3Button, raaButton, wavButton, wmaButton ]
textButtons  = [datButton, docButton, htmButton, javButton, pdfButton, wpcButton ]
packButtons  = [sezButton, rarButton, tgzButton, zipButton, rpmButton ]
mailButtons  = [dbxButton, idxButton, mbxButton, ostButton, pstButton, emaButton]
extensionButtons = [graphButtons, videoButtons, audioButtons, textButtons, packButtons, mailButtons]

def toggleExt(buttons):
    for button in buttons:
        button.toggle()

def toggleAll(state):
    for buttons in extensionButtons:
        for button in buttons:
            if state:
                button.select()
            else:
                button.deselect()


configIntro = """# Scalpel configuration file 
#
# For sample configs, check out:
# https://github.com/nolaforensix/scalpel-2.02/blob/main/scalpel2.conf
#
# For user added content, make sure the custom configs lie before the
# custom config ending marker.
#
#-------------------------BEGIN CUSTOM CONFIGS-------------------------



#--------------------------END CUSTOM CONFIGS--------------------------

"""

# Initialize Config File
def initConfig():
    with open(CONFIG_PATH, 'w') as file:
        file.write(configIntro)

def modifyConfig():
    editors = ['gedit', 'kate', 'nano', 'vim', 'emacs', 'code']
    for editor in editors:
        if subprocess.run(['which', editor], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
            write_output(f"Opened {CONFIG_PATH} with {editor}\n")
            addConfig()
            subprocess.run([editor, CONFIG_PATH])
            return
    write_output("No known text editor found on this system.\n")

def purgeConfig():
    marker = "END CUSTOM CONFIGS"
    marker_found = False
    custom_content = []

    with open(CONFIG_PATH, 'r') as file:
        for line in file:
            if marker in line:
                marker_found = True
                custom_content.append(line)
                break
            custom_content.append(line)

    with open(CONFIG_PATH, 'w') as file:
        file.writelines(custom_content)

graphButton = Button(canvas, command=lambda:toggleExt(graphButtons), text="Graphics")
videoButton = Button(canvas, command=lambda:toggleExt(videoButtons), text="Video")
audioButton = Button(canvas, command=lambda:toggleExt(audioButtons), text="Audio")
textButton  = Button(canvas, command=lambda:toggleExt(textButtons),  text="Text")
packButton  = Button(canvas, command=lambda:toggleExt(packButtons),  text="Pack")
mailButton  = Button(canvas, command=lambda:toggleExt(mailButtons),  text="Mail")
toggleButtons = [graphButton, videoButton, audioButton, textButton, packButton, mailButton]

selectAllButton    = Button(canvas, command=lambda:toggleAll(1), text="Select All")
deselectAllButton  = Button(canvas, command=lambda:toggleAll(0), text="Deselect All")
modifyConfigButton = Button(canvas, command=modifyConfig, text="Modify Config")

for button in [selectAllButton, deselectAllButton, modifyConfigButton]:
    button.config(  bg="#222222", 
                    activebackground="#111111",
                    fg="#FFFFFF", 
                    activeforeground="#AAAAAA",
                    font=("Inter", 15 * -1))

selectAllButton.place(x=510,y=320,width=130,height=30)
deselectAllButton.place(x=510,y=370,width=130,height=30)
modifyConfigButton.place(x=510,y=420,width=130,height=30)


Y_START = 300
for button in toggleButtons:
    button.config(  bg="#222222", 
                    activebackground="#111111",
                    fg="#FFFFFF", 
                    activeforeground="#AAAAAA",
                    font=("Inter", 15 * -1))
    button.place(x=40, y=Y_START, width=80, height=22)
    Y_START += 30

Y_START = 300
for buttons in extensionButtons:
    x_start = 130
    for button in buttons:
        button.config(bd=0,
                    highlightthickness=0,
                    selectcolor = "#555555",
                    bg="#393939", 
                    activebackground="#393939",
                    fg="#FFFFFF", 
                    activeforeground="#AAAAAA",
                    font=("Inter", 15 * -1))
        button.place(x=x_start, y=Y_START)
        button.select()
        x_start += 60
    Y_START += 30

extConfigs = {
    artButton: "art y 150000 \\x4a\\x47\\x04\\x0e \\xcf\\xc7\\xcb\nart y 150000 \\x4a\\x47\\x03\\x0e \\xd0\\xcb\\x00\\x00",
    bmpButton: "bmp y 100000 BM??\\x00\\x00\\x00",
    gifButton: "gif y 5000000 \\x47\\x49\\x46\\x38\\x37\\x61 \\x00\\x3b\ngif y 5000000 \\x47\\x49\\x46\\x38\\x39\\x61 \\x00\\x00\\x3b",
    jpgButton: "jpg y 200000000 \\xff\\xd8\\xff\\xe0\\x00\\x10 \\xff\\xd9\njpg y 200000000 \\xff\\xd8\\xff\\xe1 \\xff\\xd9",
    pngButton: "png y 20000000  \\x50\\x4e\\x47? \\xff\\xfc\\xfd\\xfe",
    tifButton: "tif y 200000000 \\x49\\x49\\x2a\\x00\ntif y 200000000 \\x4D\\x4D\\x00\\x2A",
    aviButton: "avi y 50000000 RIFF????AVI",
    asfButton: "asf y 8000000 \\x30\\x26\\xB2\\x75\\x8E\\x66\\xCF\\x11\\xA6\\xD9\\x00\\xAA\\x00\\x62\\xCE\\x6C",
    fwsButton: "fws y 4000000 FWS",
    movButton: "mov y 10000000 ????moov\nmov y 10000000 ????mdat\nmov y 10000000 ????widev\nmov y 10000000 ????idsc\nmov y 10000000 ????pckg",
    mpgButton: "mpg y 50000000 \\x00\\x00\\x01\\xba \\x00\\x00\\x01\\xb9\nmpg y 50000000 \\x00\\x00\\x01\\xb3 \\x00\\x00\\x01\\xb7",
    wmvButton: "wmv y 20000000 \\x30\\x26\\xB2\\x75\\x8E\\x66\\xCF\\x11\\xA6\\xD9\\x00\\xAA\\x00\\x62\\xCE\\x6C",
    mp3Button: "mp3 y 8000000 \\xFF\\xFB??\\x44\\x00\\x00\nmp3 y 8000000 \\x57\\x41\\x56\\45 \\x00\\x00\\xFF\\\nmp3 y 8000000 \\xFF\\xFB\\xD0\\ \\xD1\\x35\\x51\\xCC\\\nmp3 y 8000000 \\x49\\x44\\x33\\\nmp3 y 8000000 \\x4C\\x41\\x4D\\x45\\",
    raaButton: "ra y 1000000 .RMF\nra y 1000000 \\x2e\\x72\\x61\\xfd",
    wavButton: "wav y 200000  RIFF????WAVE",
    wmaButton: "wma y 8000000 \\x30\\x26\\xB2\\x75 \\x00\\x00\\x00\\xFF\nwma y 8000000 \\x30\\x26\\xB2\\x75 \\x52\\x9A\\x12\\x46",
    datButton: "dat y 4000000 regf\ndat y 4000000 CREG",
    docButton: "doc y 10000000 \\xd0\\xcf\\x11\\xe0\\xa1\\xb1\\x1a\\xe1\\x00\\x00 \\xd0\\xcf\\x11\\xe0\\xa1\\xb1\\x1a\\xe1\\x00\\x00 NEXT\ndoc y 10000000 \\xd0\\xcf\\x11\\xe0\\xa1\\xb1",
    htmButton: "htm n 50000 <html </html>",
    javButton: "java y 1000000 \\xca\\xfe\\xba\\xbe",
    pdfButton: "pdf y 5000000 %PDF %EOF\\x0d REVERSE\npdf y 5000000 %PDF %EOF\\x0a REVERSE",
    wpcButton: "wpc y 1000000 ?WPC",
    sezButton: "7z y 2147483648 \\x37\\x7a\\xbc\\xaf\\x27\\x1c",
    rarButton: "rar y 10000000 Rar!",
    tgzButton: "tgz y 2000000 \\x1f\\x8b\\x08\\x08",
    zipButton: "zip y 10000000 PK\\x03\\x04 \\x3c\\xac",
    rpmButton: "rpm y 1000000 \\xed\\xab",
    emaButton: "email y 4096 From:",
    dbxButton: "dbx y 10000000 \\xcf\\xad\\x12\\xfe\\xc5\\xfd\\x74\\x6f",
    idxButton: "idx y 10000000 \\x4a\\x4d\\x46\\x39",
    mbxButton: "mbx y 10000000 \\x4a\\x4d\\x46\\x36",
    ostButton: "ost y 500000000 \\x21\\x42\\x44\\x4e",
    pstButton: "pst y 500000000 \\x21\\x42\\x4e\\xa5\\x6f\\xb5\\xa6"
}




# RUN
# Text widget to display the output
cmdOutput = Text()
cmdScroll = Scrollbar(cmdOutput, command=cmdOutput.yview)

cmdOutput.config(padx=3, pady=3, yscrollcommand=cmdScroll.set, state="disabled")
cmdOutput.place(x=0, y=480, height=180, width=670)
cmdScroll.pack(side=RIGHT, fill=Y)

def openOutputDir():
    output_dir = outputBox.get()
    file_managers = ['nautilus', 'dolphin', 'thunar', 'pcmanfm', 'nemo']
    for manager in file_managers:
        if subprocess.run(['which', manager], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
            write_output(f"Opened Output directory {output_dir} with {manager}\n")
            subprocess.run([manager, output_dir])
            return
    write_output("No known file manager found on this system.\n")

def write_output(text):
    cmdOutput.config(state="normal")
    cmdOutput.insert(END, text)
    cmdOutput.config(state="disabled")
    cmdOutput.yview(END)

def update_output(proc):
    def _update_output():
        for line in proc.stdout:
            write_output(line.decode())
    return _update_output

def update_output(proc):
    def _update_output():
        try:
            for line in proc.stdout:
                decoded_line = line.decode()
                write_output(decoded_line)
                if "Scalpel is done" in decoded_line:
                    openOutputDir()
                    proc.terminate()
                    break
        finally:
            proc.stdout.close()
    return _update_output

def addConfig():
    purgeConfig()
    with open(CONFIG_PATH, 'a') as file:
        for buttons in extensionButtons:
            for button in buttons:
                if int(button.getvar(button.cget('variable'))) == 1:
                    file.write(extConfigs[button] + '\n')

def run_command(command):
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    thread = threading.Thread(target=update_output(proc))
    thread.start()

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
def execute():
    if inputBox.get() == "":
        write_output("Please Choose an Input File\n")
        return

    command = f"./_internal/scalpel2 -c ./scalpel.conf {inputBox.get()}"
    if outputBox.get() == "":
        write_output("Defaulting Output Directory to ./scalpel-output\n")
        outputBox.insert(0,OUTPUT_PATH / Path("scalpel-output"))
    else:
        command += f" -o {outputBox.get()}"
    
    if (OPTION_Q.get()):
        arg = qEntry.get().strip()
        if arg == "":
            write_output("Please Input the Cluster Size for Alignment.\n")
            return
        elif not is_int(arg):
            write_output("The Cluster Size needs to be an Integer.\n")
            return
        else:
            command += " -q " + qEntry.get()
    
    if (OPTION_B.get()):
        command += " -b"
    if (OPTION_D.get()):
        command += " -d"
    if (OPTION_E.get()):
        command += " -e"
    if (OPTION_N.get()):
        command += " -n"
    if (OPTION_O.get()):
        command += " -O"
    if (OPTION_P.get()):
        command += " -p"
    if (OPTION_R.get()):
        command += " -r"
    
    write_output(f"RUNNING: {command} \n====================\n")
    addConfig()
    run_command(command)
    

runButton = Button(
    borderwidth=0,
    highlightthickness=0,
    command=execute,
    bg="#DDDDDD", 
    activebackground="#FFFFFF",
    fg="#333333", 
    activeforeground="#222222",
    font=("Inter Bold", 28 * -1),
    text="RUN",
    relief="groove"
)

runButton.place(x=270.0, y=670.0, width=130.0, height=40.0)
initConfig()
window.resizable(False, False)
window.mainloop()
