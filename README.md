# Real-time Sign Language Translator
The software is designed to enable text input through hand sign language recognition, eliminating the need for physical interaction with a keyboard. Utilizing the device’s front-facing camera, the program detects hand signs made by the user. The software translates them into corresponding alphabetic characters (a–z) or special characters such as "Space", "Delete", and "Period". Each alphabetic character is added one at a time to a word's auto-completion algorithm.

As the user enters more alphabetic characters to construct a word, the software dynamically offers word suggestions, which are updated in real time as new characters are added. Users can select a suggested word from the list or continue inputting additional characters to find the desired word. Once a word is selected, it is appended to the final output area, allowing the user to build complete sentences. Additionally, the user can use the special characters of "Space" and "Period" to write full sentences. The finalized text can then be copied for use elsewhere.

Below is the translation from hand signs to characters:

<img src="https://github.com/SirAbsolute0/Realtime_Sign_Language_Translator/raw/main/software_description/Hand_Sign_Description_0.jpg" width="600" height="800"/>
<img src="https://github.com/SirAbsolute0/Realtime_Sign_Language_Translator/raw/main/software_description/Hand_Sign_Description_1.jpg" width="600" height="800"/>
<img src="https://github.com/SirAbsolute0/Realtime_Sign_Language_Translator/raw/main/software_description/Hand_Sign_Description_2.jpg" width="600" height="800"/>

## How It's Made:

**Tech used:** Python, PyQt, Open-CV, MediaPipe, Pytorch, Trie Node DS, and others

The GUI is built using PyQt Designer with a combination of QtWidgets (QLayout, QLabel, QListWidget, QButton, etc). The backend utilizes Python to handle all logic using QtSignals and QtSlots. The hand landmark detection is handled by Google's MediaPipe model, which detects 23 landmarks per hand through the front-facing camera using Open-CV. The software currently only supports hand signs made using the left hand. After the software detects the 23 landmarks, the data is pushed to a Pytorch Neural Network model running on a GPU to translate the landmarks to a character in the alphabet. As the user enters more characters to build a word, the software dynamically searches its dictionary, tries to auto-complete the word, and suggests possible words to the user. The word dictionary is built on a Trie Node data structure, which is loaded at startup with over 10,000 words.

## Optimizations
Initially, I utilized a random forest model to translate the MediaPipe result of 23 hand landmarks to a character, which displayed great promise in the accuracy result of the validation dataset. However, the live model using random forest didn't perform well and would get a lot of misdetections. Thus, I decided to switch to a neural net model since the fundamental idea of a neural net model is more aligned with the software's purpose compared to a random forest model. Specifically, a random forest model decision is based on data being passed and checked through each branch of a decision tree, and the final decision is made with the overall decision of all trees. Since the data is being passed along 1 at a time down the branches, the data has to be sequentially related. However, each hand landmark is not related sequentially, each hand landmark should have the same weight in deciding the final output of the character, so making a decision at each branch with only 1 hand landmark and making another decision at a later branch with another hand landmark can't utilize the hand landmarks well. On the other hand, a neural net model input can be multiple variables, and all are considered at once. Therefore, all 23 landmarks can be considered at every layer to better translate into a character.

During training the neural net model with Pytorch, I specifically took the long route to practice some key skills in machine learning to optimize my model and software, which are: 
1. Run all models with GPU (hardware acceleration): The initial random forest model was run on CPU, while the current neural net model runs on GPU. Although it is possible to also run the neural net model on a CPU and still get decent performance, it is good practice for a neural net model, even for a simplified model like mine, to be running on a GPU.
2. Saving a model's state and continuing training on a new dataset: At each step of the training, I section off a folder specifically for training the model of that version. Example: neural_net_model_ver2, neural_net_model_ver2.1, etc. For folders with same starting version (in this case version 2), the changes between the models are purely improvements (meaning training with similar data for better performance). 
3. Expanding classification categories of a pre-trained model when needed: For folders with different starting version (ver1, ver2, and ver3, etc), the changes between models are significant (meaning the model structure itself change or something major within the model changed). During version 2 to version 3, I expanded the classfication categories from 26 (a-z) to 29 to accommadate new special characters and the change in version signifies major change in the model structure.
4. Comparing results between various models and determining which model is the best for the latest version: The more models I trained, the more I realized how difficult it is to keep track of every possible results of each model, especially when those results are scattered throughout different jupyter notebook files. Thus, in the next project, I will implement a mlops techniques to support model development. 
   
Another optimization I made as I was building the software was the usage of a Trie Node for the auto-completion search tree. I came across this data structure as I was studying leetcode for upcoming interviews and realized how useful it is in use cases such as my software where the initial loading time might take awhile (with loading 10,000 words into a tree), the auto-completion for each word is almost in constant time and can be done quickly as the user enter more and more character without bogging down the user with wait time. 

## Lessons Learned:
Some of the key lessons I learned are:
1. Choosing the correct machine learning model for the task
2. Leetcode data structure can be useful in real, day-to-day engineering development.
3. It's not about having the perfect software, instead, it's about having a complete software package that serves a purpose and can improve over time.
4. Training and improving machine learning models require rigorous organization and data management.
5. There will always be more improvements to make.


