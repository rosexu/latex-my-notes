# Latex My Notes

Latex My Notes is a project built in 36 hours at MHacks. It is a native iOS app and a web app that allows the user to upload a picture of printed notes from their phone and our app will automatically convert that picture into a latex PDF file. 

**Inspiration**
I wanted to ctrl-F my written notes

**How it was built**
My teammate made the iOS app. I wrote the server-side python code that takes the picture from the POST request and use tesseract(an open-source OCR technology) to take the text and convert it to a latex file with a predefined format and lastly stores it in MongoDB. I also wrote the front-end code for the web application that shows all the files that are converted to latex. 
Technologies used: Flask(python) for server, js for front-end, tesseract for OCR, MongoDB for data storage and queries

**Challenges**
Originally, we wanted to make this work for hand-written notes. Imagine being able to take a picture of your friend's notes and have it instantly in pretty latex format and that is searchable. However, we realized half way through building this app that current OCR technology are not advanced enough to support accurate character recognition for handwriting so we settled for printed notes but even then the accuracy is not 100%. Looks like computer vision still has a long way to go. 

**What I learned**
I became much more familiar with Flask and MongoDB, learned how to integrate with open-source software. 