# YouTube Mass Unsubscribe Tool
The YouTube Mass Unsubscribe Tool is a tool which uses the official Google Cloud YT API - specifically, the YouTube Data v3 API - to unsubscribe from any YouTube channels you may be subscribed to.
This tool is written in Python and provides a simple GUI achieved with the help of tkinter.
<br><br>
All you need to do is to add the project in your Google Cloud Account (easy) and then download the client-secret.json file.
Then, insert it using the app's built-in function and the app will open a Authentication dialog, and you need to click Allow to give the app permissions to unsubscribe from your accounts.
That's all! You should be able to click Start and the app will start unsubscribing from the channels.
<br><br>
I plan to build onto this over time, adding cool features.
<br>

- [ ] Whitelisting (Channels you DON'T want to unsubscribe from)
<br>

- [ ] A Dark Mode for all platforms (in development)

# Getting the client-secret.json file
Getting the client-secret.json file is pretty simple.
Here's the overview of what you need to do:
* Create a Google Cloud project and setup the app.
* Download the client-secret.json file
* Add it to the program
<br>
The program also has a link to a quick 3-minute video which shows step-by-step of how to create the project and download the file.
<br><br>

# Download Links
<br>
Here are some download links for Windows and Mac (Linux version will be here soon):<br>
<a href="https://github.com/crazycheetah42/YTMassUnsubscribeTool/releases/download/v1.0.0/YT_Mass_Unsubscriber_win_amd64.exe">Windows (exe)</a>
<br>
<a href="https://github.com/crazycheetah42/YTMassUnsubscribeTool/releases/download/v1.0.0/YT_Mass_Unsubscriber_Mac.dmg">Mac (dmg)</a>
<br><br>
<i>Note: If you are using the Google Cloud free API and have more than 200 channels subscribed to, you will only get 200 channels unsubscribed each day, so if you have more you can either pay in Google Cloud for more tokens, or wait for the next day to continue.</i>
<br><br>

![Screenshot 2024-02-04 093419](https://github.com/crazycheetah42/YTMassUnsubscriber/assets/76403763/ae71c418-55d5-4b0a-b835-88503861e5e3)
