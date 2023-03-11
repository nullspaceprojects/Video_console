
1) Download CircuiPython: adafruit-circuitpython-raspberry_pi_pico-it_IT-8.0.2.uf2
2) Plug In the Pico and Load the above uf2 file in the Pico drive that appears
3) The Pico drive will disappear and a new disk drive called CIRCUITPY will appear.
4) Download the library bundle adafruit-circuitpython-bundle-8.x-mpy-20230223.zip
5) Unzip it and in the "lib" folder search for the library "adafruit_hid"
6) Plug In the Pico if not yet plugged-in, it will appear the drive CIRCUITPY.
7) Inside this drive find the "lib" folder. Copy inside the "lib" folder the folder 	"adafruit_hid" found in 5).
8) Download the main script "code.py" that is inside the "code" folder
9) Inside CIRCUITPY drive of the plugged Pico, copy (or replace) the python script "code.py" just downloaded
10) Download and Install "MuEditor-win64-1.2.0.msi", the IDE to write our python scripts for the Pico (https://codewith.mu/)
11) Once Installed, Open it and click the Mode botton (upper left in the Mu program). Choose CircuitPython as programming language.
12) With the Mu editor you can open the code.py code and edit it. If the Pico is plugged in, you can directly download the modified code in the Pico. Moreover you can open the serial to print what the Pico is writing.
13) To Uninstall the CircuitPython from the Pico, hold the Pico Button, connect the board to PC, release the Pico Button, copy the flash_nuke.uf2 inside folder that appears.

puo' succedere che il dispositivo viene riconosciuto da windows ma non e' funzionante.
in questo caso dovete andare in PANNELLO DI CONTROLLO - HARDWARE E SUONI - DISPOSITIVI E STAMPANTI
selezionare l'icona della tastiera chiamata PICO e cliccare con il tasto dx del mouse e selezionare PROPRIETA.
Si aprirà una finestra e cliccate sul tab HARDWARE.
selezionate la voce DISPOSITIVO DI ARCHIVIAZIONE DI MASSA USB e cliccare PROPRIETà.
Nel tab GENERALE cliccate CAMBIA IMPOSTAZIONI.
Nel tab DRIVER cliccate DISABILITA DISPOSITIVO.
e la tastiera inizierà a funzionare.
