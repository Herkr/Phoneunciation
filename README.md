# Phoneunciation
Screenshot of Phoneunciation application
![Architecture](https://github.com/Herkr/Phoneunciation/blob/main/Phoneunciation_application.png)

This application uses Allosaurus to transcribe phones from audio files. 
Allosaurus can be found here: https://github.com/xinjli/allosaurus/tree/master

For the code to work, you have to:
1. Install the missing packages.
2. Create a folder called "words" and add .wav audio files to the folder. These are the reference words.
3. Train a new model in Allosaurus in faroese and call it 'fa2024'.
4. Update the exsisting 'fao' language in Allosaurus to match the phones used in the model.

The .wav audio files used in this project are not to be published from the main source. Therefore the .wav files are not published here.
