# video_to_text
Extract Speech/Text from Video to text file(.txt)
#

## Installation and Usage
### 1- Downloading from Pypi
`pip install video-to-text-vtt`
and then you can run it as:
script: `vtt_run [OPTIONS] path/to/YourVideo` or module: `python -m video_to_text_VTT [OPTIONS] path/to/YourVideo`

### 2- Using poetry 
`git clone https://github.com/momalekiii/VTT.git`
and then 
`poetry install`
and then you can run it by 
`poetry run vtt_run [OPTIONS] path/to/YourVideo` or `poetry run python -m video_to_text_VTT [OPTIONS] path/to/YourVideo`

### 3- Using pip [locally]
`git clone https://github.com/momalekiii/VTT.git`
and then 
`pip install -r requirements.txt`
and then you can run it by 
`python main.py [OPTIONS] path/to/YourVideo`

## [OPTIONS]
* --duration FLOAT        Audio length [seconds]
* --offset FLOAT          How far from zero you start [seconds]
* -lang, --language TEXT  Audio language. Supported languages can be found in
                          <http://stackoverflow.com/a/14302134>
* -o, --output TEXT       The result file
* --help                  Show this message and exit.

