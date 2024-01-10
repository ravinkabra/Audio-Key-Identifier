from pymusickit.key_finder import KeyFinder
from pydub import AudioSegment
import os
import PySimpleGUI as sg
import atexit

def scale_check(audio_path):
    try:
        song = KeyFinder(audio_path)
        song.print_key()
        key = song.get_primary_key_corr()
        alt = song.get_secondary_key_corr()
      
        sg.Print("Primary key: " + str(key), "\n" + "Alt Key: " + str(alt))


        
        song.print_chroma()
        song.print_corr_table()
        show_chromagram = sg.popup_yes_no('Do you want to see the chromagram?', title='Chromagram Display')

        if show_chromagram == 'Yes':
            song.show_chromagram(title="Your Recorded Audio")
    except Exception as e:
        print(f"Error: {e}")

def main():
    sg.theme('LightGrey1')

    layout = [
        [sg.Text('Select an audio file:')],
        [sg.InputText(key='file_path', enable_events=True), sg.FileBrowse()],
        [sg.Button('Check Scale'), sg.Exit()]
    ]

    window = sg.Window('Audio Scale Checker', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
        elif event == 'Check Scale':
            file_path = values['file_path']
            
            if os.path.exists(file_path):
                # Only convert if the input file is not in MP3 format
                if not file_path.lower().endswith('.mp3'):
                    output_file = 'output.mp3'  # You can customize the output file name

                    if os.path.exists(output_file):
                        sg.popup_error(f"The file '{output_file}' already exists in the directory.")
                    else:
                        audio = AudioSegment.from_file(file_path)
                        audio.export(output_file, format="mp3")
                        scale_check(output_file)
                        atexit.register(lambda: os.remove(output_file))
                else:
                    scale_check(file_path)
            else:
                sg.popup_error('File does not exist. Please select a valid audio file.')

    window.close()

if __name__ == '__main__':
    main()
