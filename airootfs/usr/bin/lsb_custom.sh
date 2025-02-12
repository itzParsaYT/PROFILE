rm -rf /etc/lsb-release
mv /usr/bin/lsb_custom_conf /etc/lsb-release
pip install pydub thefuzz speechbrain transformers ffmpeg-python sv_ttk darkdetect --break-system-packages 
pip install git+https://github.com/openai/whisper.git git+https://github.com/mmabrouk/chatgpt-wrapper.git --break-system-packages
mv lib/py_libs lib/python3.13
