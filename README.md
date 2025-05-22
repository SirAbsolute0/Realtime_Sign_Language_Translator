# Real-time Sign Language Translator
The software is designed to enable text input through hand sign language recognition, eliminating the need for physical interaction with a keyboard. Utilizing the device’s front-facing camera, the program detects hand signs made by the user and translates them into corresponding alphabetic characters (a–z). These characters are sequentially added to form a word-in-progress.

As the user constructs a word, the software dynamically offers word suggestions through an auto-completion feature, which updates in real time as new characters are detected. Users may either select a suggested word from the list or continue inputting additional characters. Once a word is selected, it is appended to the final output area, allowing the user to build complete sentences. The finalized text can then be copied for use elsewhere.

![First set of characters](https://github.com/SirAbsolute0/Realtime_Sign_Language_Translator/blob/main/hand_description_0.jpg)
![Second set of characters](https://github.com/SirAbsolute0/Realtime_Sign_Language_Translator/blob/main/hand_description_1.jpg)
![Third set of characters](https://github.com/SirAbsolute0/Realtime_Sign_Language_Translator/blob/main/hand_description_3.jpg)
## How It's Made:

**Tech used:** Python, PyQt, cv2, MediaPipe, Pytorch, Trie Node DS

The GUI is built with PyQt Designer with a combination of QtWidgets (QLayout, QLabel, QListWidget, QButton, etc). The backend utilizes Python to handle all logic using QtSignals and QtSlots. The hand landmark detection is handled by Google's MediaPipe model, which detects 23 landmarks per hand through the front-facing camera with OpenCV. The software currently only supports hand signs made using the left hand. After the software detects the 23 landmarks, the data is pushed to a Pytorch Neural Network model to translate the landmarks to a character in the alphabet. The hand sign to character table is shown above in the software description. As the user enters more characters to build a word, the software dynamically searches its dictionary, tries to auto-complete the word, and suggests it to the user. The word dictionary is built on a Trie Node data structure, which is loaded at startup with over 10,000 words.

## Optimizations
Initially, I utilized a random forest model to translate from the 23 hand landmarks to a character, which showed to work great based on the accuracy result of the validation data set (correct predictions/all predictions). However, the live model didn't perform well and would get a lot of missed detections (detect wrong characters). Thus, I decided to switch to a neural net model since the fundamental idea of a neural net model is more aligned with the software's purpose compared to a random forest model. Specifically, a random forest model decision is based on data being passed and checked through each branch  of a decision tree, and the final decision is made with the overall decision of all trees. Since the data is being passed along 1 at a time down the branches, the data has to be sequentially related. However, each hand landmark is not related sequentially, each hand landmark should have the same weight in deciding the final output of the character, so making a decision at each branch with only 1 hand landmark and making another decision at a later branch with another hand landmark can't utilize the hand landmarks well. On the other hand, a neural net model input can be multiple variables, and all are considered at once. All 23 landmarks can be considered at once at every layer to better translate into a character.

Another optimization I made as I was building the software was the usage of a Trie Node for the auto-completion search tree. I came across this data structure as I was studying leetcode for upcoming interviews and realized how useful it is in use cases such as my software where the initial loading time might take awhile (with loading 10,000 words into a tree), the auto-completion for each word is almost in constant time and can be done quickly as the user enter more and more character without bogging down the user with wait time. 

## Lessons Learned:
Some of the key lessons I learned are:
1. How important is choosing the correct machine learning model for a problem.
2. Leetcode data structure can be useful in real day-to-day engineering development.
3. Its not about having the perfect software but about having a complete software package that serves a purpose and can improve overtime.



