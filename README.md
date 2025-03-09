# Songsterr_tabs_extractor

 Download all your favorites saved tabs from Songsterr, organize it by Artist and save each tab with the Artist and Title name of the song.

## Installation

```bash
git clone https://github.com/C0deInBlack/Songsterr_tabs_extractor.git
pip install -r requirements.txt
```

## Usage

```bash
usage:
        ./main.py <temp mail> <json path> <path to save>
```

The script takes three arguments, a temporary email, the path of your JSON Songsterr data and the path where you want to save the tabs.

As Songsterr requires a registered account for download tabs, you can use any temporary email server, for example [1secmail](https://www.1secmail.cc/).

For export your JSON file, go to your Songsterr [account](https://www.songsterr.com/a/wa/account) and click in 'Download my data'.

If the script fail, you will need to retry it with a new temporary email, [1secmail](https://www.1secmail.cc/) makes easy regenerate emails.
