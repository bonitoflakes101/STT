# STT
Speech to Text using pvrecorder for recording audio and whisper AI for transcribing it into text

SETUP
  1.) In CLI, do this:
  
      pip install pvrecorder
      pip install openai

      if this doesn't work then do:

      python -m pip install pvrecorder
      python -m pip install openai(new version na gamit)
  
  2.) Create your own API key (ask harley, he will give u access). Then replace your own API key sa variable sa code

  3.) Good to run na

HOW DOES IT WORK?

  1.) Pag ka run, mag di-display yung available mics to use. For now, yung mic ng laptop gamit ko where device_index=0. Edit nalang if ibang mic gagamitin
  
  2.) Then mag re-record na agad, user speaks then press ENTER for it to stop. (OR para mag stop press ulit record button, to be added pa)
  
  3.) After stopping, may transcribed text na to be displayed.

FUTURE IMPROVEMENTS?

  1.) openai 0.28 gamit ko which is NOT the new version, this uses the openai.Audio.transcribe function. Ito palang napagana ko. 
      -  try to find new alternatives sa openai.Audio.transcribe, this requires you to install the newest openai sa CLI (NVM THIS)
      
  2.) Sa user recording, instead na ENTER yung ipress to stop. Dapat ata sa button siya. Research abt it. 
