# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.3.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---


# %%
#!pip install  pyannote.audio pydub  scipy soundfile torchvision speechbrain setuptools-rust
#!pip install -U openai-whisper
#https://huggingface.co/pyannote/speaker-diarization
#https://huggingface.co/speechbrain/sepformer-wsj02mix
#https://github.com/openai/whisper
# %% diarisation
# diarization
from pyannote.audio import Pipeline
import os
import torch
from pydub import AudioSegment
import numpy as np
from speechbrain.pretrained import SepformerSeparation as separator
import whisper
import json
import torchaudio
import argparse
#from option import parse
def split_wav_by_time(input_file, output_file, start_time, end_time):
    # Load the input .wav file
    sound = AudioSegment.from_wav(input_file)

    # Extract the segment of the sound between the start and end times
    segment = sound[start_time*1000:end_time*1000]

    # Export the segment to a new .wav file
    segment.export(output_file, format="wav")
# Example usage: split a 10-second .wav file from 2 seconds to 8 seconds

def sol(fn,hf_token,output_fn):
  directory = "output"
  #if not os.path.exists(directory):
    #os.makedirs(directory)
  try:
    os.mkdir(directory)
    print("Directory created successfully.")
  except FileExistsError:
    print("Directory already exists.")
  except Exception as e:
    print("Error:", e)

  os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
  print("start")
  device = torch.device("cpu" if torch.cuda.is_available() else "cpu")
  pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization",
                                      use_auth_token=hf_token)
  INPUT=fn
  print("start diarization")
  diarization = pipeline(INPUT)
  transcript=[]
  transcript2=[]
  for turn, _, speaker in diarization.itertracks(yield_label=True):
      #print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
      transcript.append([turn.start,turn.end,int(speaker[-1])])
      transcript2.append([turn.start,turn.end,int(speaker[-1])])
  print("finished diarization")
# %%  speech separator
  print("start separation")
  model = separator.from_hparams(source="speechbrain/sepformer-wsj02mix", savedir='pretrained_models/sepformer-whamr')
  est_sources = model.separate_file(path=fn) 
  torchaudio.save("./output/0.wav", est_sources[:, :, 0].detach().cpu(), 8000)
  torchaudio.save("./output/1.wav", est_sources[:, :, 1].detach().cpu(), 8000)
  #print(transcript)
  print("finished separation")
# %% cut sep audio by diarisation 1
  print("start speech to text")
  for i in range(len(transcript)):
    split_wav_by_time("./output/"+str(transcript[i][2])+".wav","./output/diarization_"+str(i)+".wav",transcript[i][0],transcript[i][1])
    transcript[i].append("./output/diarization_"+str(i)+".wav")
    #print("./",INPUT.split('/')[-1],"diarization_"+str(i),transcript[i][0],transcript[i][1])
  #print(transcript)
# %% speech2text 1
  model = whisper.load_model("medium.en")
  for i in range(len(transcript)):
    result = model.transcribe(transcript[i][3])
    transcript[i].append(result["text"])
    #print(transcript[i])
  #print(transcript)
# %% cut sep audio by diarisation 2
  for i in range(len(transcript2)):
    split_wav_by_time("./output/"+str(int((transcript2[i][2]-1)**2))+".wav","./output/diarization2_"+str(i)+".wav",transcript2[i][0],transcript2[i][1])
    transcript2[i].append("./output/diarization2_"+str(i)+".wav")
    #print("./",INPUT.split('/')[-1],"diarization2_"+str(i),transcript2[i][0],transcript2[i][1])
  #print(transcript2)
# %% speech2text 2
  for i in range(len(transcript2)):
    result = model.transcribe(transcript2[i][3])
    transcript2[i].append(result["text"])
    #print(transcript2[i])
  #print(transcript2)
# %%
  if output_fn[-5:]!='.json':
    output_fn+=".json"
  print("output: ",output_fn)
  transcript=np.array(transcript)
  str1=''.join(transcript[0:(len(transcript)) ,-1:].reshape(-1))
  transcript2=np.array(transcript2)
  str2= ''.join(transcript2[0:(len(transcript2)) ,-1:].reshape(-1))
  if len(str1)>len(str2):
    winner=transcript
  else:
    winner=transcript2
  print(winner)
  dict_winner = [{'start_time': item[0], 'end_time': item[1], 'speaker': item[2], 'file_name': item[3], 'text': item[4]} for item in winner]
# %%
  with open(output_fn, 'w') as f:
    json.dump(dict_winner, f)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument(
      '--wav', type=str, default='./example.wav', help='Path to .wav file.')
    parser.add_argument(
      '--hf_token', type=str, default="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", help='huggingface token; follow the intructions at #https://huggingface.co/pyannote/speaker-diarization')
    parser.add_argument(
      '--output', type=str, default="output", help='Place the output into file.')
    args=parser.parse_args()
    sol(args.wav,  args.hf_token,args.output)
if __name__ == "__main__":
    main()
