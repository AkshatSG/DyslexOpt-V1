import pyaudio
import wave
import keyboard
import whisper
import requests
import termios
import time
import sys
from itertools import zip_longest

sp = []
acc = []
flu = []
rew = []
comf = []


#Reading texts generated from Mistral 7B
paragraphs = [
    ["Once", "upon", "a", "time,", "in", "a", "small", "village", "by", "the", "sea,", "there", "lived", "an", "old", "fisherman", "named", "Tom.", "Tom", "had", "a", "big,", "friendly", "dog", "named", "Max.", "Every", "morning,", "Tom", "and", "Max", "would", "go", "fishing", "in", "their", "little", "boat.", "They", "loved", "the", "quiet", "of", "the", "early", "morning", "hours."],
    ["In", "the", "middle", "of", "the", "village,", "there", "was", "a", "tall,", "ancient", "oak", "tree.", "Children", "loved", "to", "play", "under", "its", "branches,", "and", "birds", "made", "their", "nests", "in", "its", "leaves.", "One", "day,", "a", "magician", "came", "to", "the", "village.", "He", "was", "tall", "and", "wore", "a", "cloak", "covered", "in", "stars", "and", "moons."],
    ["The", "magician", "set", "up", "a", "tent", "in", "the", "village", "square.", "He", "promised", "to", "show", "amazing", "tricks", "and", "cast", "spells.", "Everyone", "was", "excited", "and", "gathered", "around.", "With", "a", "wave", "of", "his", "wand,", "he", "made", "a", "bird", "appear", "from", "his", "hat.", "Then,", "he", "pulled", "a", "rabbit", "from", "his", "pocket.", "The", "crowd", "cheered."],
    ["Tom", "and", "Max", "watched", "in", "amazement.", "The", "magician", "saw", "them", "and", "smiled.", "\"Would", "you", "like", "to", "see", "a", "special", "trick?\"", "he", "asked.", "Tom", "nodded.", "The", "magician", "handed", "Tom", "a", "magic", "stone.", "\"Make", "a", "wish,\"", "he", "said.", "Tom", "wished", "for", "a", "big", "fish.", "The", "stone", "glowed,", "and", "suddenly,"],
    ["a", "huge", "fish", "jumped", "into", "Tom's", "boat.", "Tom", "and", "Max", "were", "thrilled.", "\"Thank", "you,\"", "Tom", "said", "to", "the", "magician.", "The", "magician", "smiled", "and", "nodded.", "\"Use", "the", "stone", "wisely,\"", "he", "advised.", "Tom", "and", "Max", "went", "home,", "eager", "to", "tell", "their", "friends", "about", "the", "magic", "stone", "and", "the", "big", "fish."],
    ["The", "next", "day,", "Tom", "decided", "to", "explore", "a", "new", "part", "of", "the", "sea.", "He", "and", "Max", "sailed", "farther", "than", "they", "ever", "had", "before.", "They", "discovered", "a", "beautiful", "island", "with", "golden", "sands", "and", "lush", "green", "trees.", "On", "the", "island,", "they", "found", "a", "treasure", "chest", "buried", "in", "the", "sand."],
    ["Tom", "used", "the", "magic", "stone", "to", "open", "the", "chest.", "Inside,", "they", "found", "glittering", "jewels", "and", "gold", "coins.", "Tom", "couldn't", "believe", "his", "eyes.", "\"We're", "rich,\"", "he", "exclaimed.", "Max", "barked", "happily.", "They", "decided", "to", "bring", "the", "treasure", "back", "to", "the", "village", "to", "share", "with", "their", "friends."],
    ["When", "they", "returned", "home,", "the", "villagers", "were", "amazed", "by", "the", "treasure.", "They", "thanked", "Tom", "and", "Max", "for", "their", "generosity.", "The", "village", "celebrated", "with", "a", "grand", "feast.", "There", "was", "dancing,", "singing,", "and", "laughter.", "Everyone", "was", "happy.", "Tom", "and", "Max", "felt", "proud", "and", "content.", "They", "knew", "they", "had", "done", "something", "good."],
    ["One", "day,", "a", "storm", "hit", "the", "village.", "The", "wind", "howled", "and", "the", "waves", "crashed", "against", "the", "shore.", "Tom", "and", "Max", "worked", "together", "to", "help", "their", "neighbors.", "They", "secured", "boats,", "mended", "roofs,", "and", "comforted", "those", "who", "were", "scared.", "The", "storm", "was", "fierce,", "but", "they", "stayed", "brave", "and", "strong."],
    ["After", "the", "storm", "passed,", "the", "village", "was", "damaged,", "but", "no", "one", "was", "hurt.", "The", "villagers", "came", "together", "to", "repair", "the", "damage.", "Tom", "and", "Max", "led", "the", "efforts,", "working", "tirelessly.", "They", "used", "the", "magic", "stone", "to", "help", "speed", "up", "the", "repairs.", "Soon,", "the", "village", "was", "restored."],
    ["Life", "in", "the", "village", "returned", "to", "normal.", "Tom", "and", "Max", "continued", "their", "fishing", "trips,", "always", "finding", "new", "adventures.", "They", "knew", "the", "magic", "stone", "was", "a", "great", "gift,", "but", "they", "also", "knew", "the", "true", "magic", "was", "in", "their", "friendship", "and", "their", "bravery.", "Together,", "they", "could", "face", "anything."],
    ["One", "morning,", "Tom", "and", "Max", "set", "out", "early.", "The", "sky", "was", "clear,", "and", "the", "sea", "was", "calm.", "They", "sailed", "to", "a", "new", "fishing", "spot", "they", "had", "heard", "about.", "As", "they", "waited", "for", "fish", "to", "bite,", "Tom", "told", "Max", "stories", "of", "his", "youth."],
    ["Max", "listened", "attentively,", "his", "ears", "perked", "up.", "He", "loved", "hearing", "about", "Tom's", "adventures", "and", "dreamed", "of", "having", "his", "own.", "Suddenly,", "they", "felt", "a", "strong", "tug", "on", "the", "line.", "Tom", "reeled", "in", "a", "massive", "fish.", "It", "was", "the", "biggest", "they", "had", "ever", "caught."],
    ["They", "returned", "to", "the", "village", "with", "their", "prize.", "The", "villagers", "were", "amazed", "by", "the", "size", "of", "the", "fish.", "They", "prepared", "a", "feast", "to", "celebrate.", "Tom", "and", "Max", "were", "the", "heroes", "of", "the", "day.", "Everyone", "cheered", "for", "them.", "It", "was", "a", "day", "to", "remember."],
    ["As", "the", "years", "went", "by,", "Tom", "and", "Max", "continued", "to", "have", "many", "adventures.", "They", "explored", "new", "places,", "met", "new", "friends,", "and", "always", "helped", "those", "in", "need.", "Their", "reputation", "grew,", "and", "they", "became", "known", "as", "the", "bravest", "duo", "in", "the", "land."],
    ["One", "day,", "they", "received", "a", "letter", "from", "a", "distant", "kingdom.", "The", "king", "needed", "their", "help.", "His", "kingdom", "was", "under", "threat", "from", "a", "terrible", "dragon.", "Tom", "and", "Max", "didn't", "hesitate.", "They", "packed", "their", "bags", "and", "set", "off", "on", "their", "next", "big", "adventure."],
    ["The", "journey", "was", "long", "and", "arduous,", "but", "they", "were", "determined.", "They", "crossed", "mountains,", "rivers,", "and", "deserts.", "Along", "the", "way,", "they", "met", "many", "kind", "people", "who", "offered", "them", "shelter", "and", "food.", "Finally,", "they", "reached", "the", "kingdom", "and", "were", "greeted", "by", "the", "grateful", "king."],
    ["The", "king", "explained", "that", "the", "dragon", "was", "a", "fearsome", "creature,", "breathing", "fire", "and", "destroying", "everything", "in", "its", "path.", "Tom", "and", "Max", "listened", "carefully.", "They", "knew", "they", "had", "to", "be", "brave.", "The", "king", "gave", "them", "a", "magical", "sword", "and", "a", "shield", "to", "help", "them."],
    ["Armed", "with", "the", "magical", "weapons,", "Tom", "and", "Max", "set", "off", "to", "find", "the", "dragon.", "They", "followed", "the", "trail", "of", "destruction", "until", "they", "reached", "its", "lair.", "The", "dragon", "was", "huge,", "with", "scales", "as", "hard", "as", "iron.", "It", "roared", "when", "it", "saw", "them,", "breathing", "fire."],
    ["Tom", "raised", "the", "magical", "shield,", "deflecting", "the", "fire,", "while", "Max", "darted", "around", "to", "distract", "the", "dragon.", "With", "a", "swift", "move,", "Tom", "struck", "the", "dragon", "with", "the", "magical", "sword.", "The", "dragon", "let", "out", "a", "mighty", "roar", "and", "fell", "to", "the", "ground."],
    ["The", "kingdom", "was", "saved.", "The", "king", "thanked", "Tom", "and", "Max", "for", "their", "bravery.", "They", "were", "rewarded", "with", "gold", "and", "gems,", "but", "more", "importantly,", "they", "gained", "the", "gratitude", "and", "friendship", "of", "the", "king", "and", "his", "people.", "Tom", "and", "Max", "returned", "home", "as", "heroes."],
    ["Back", "in", "their", "village,", "they", "were", "welcomed", "with", "open", "arms.", "The", "villagers", "celebrated", "their", "return", "with", "another", "feast.", "Tom", "and", "Max", "shared", "stories", "of", "their", "adventures.", "Everyone", "listened", "in", "awe.", "They", "knew", "that", "Tom", "and", "Max", "were", "truly", "special.", "Their", "legend", "grew."],
    ["Years", "passed,", "and", "Tom", "grew", "older.", "Max", "was", "still", "by", "his", "side,", "faithful", "and", "strong.", "They", "continued", "to", "help", "their", "village,", "always", "ready", "for", "a", "new", "adventure.", "They", "knew", "that", "as", "long", "as", "they", "were", "together,", "they", "could", "face", "any", "challenge."],
    ["One", "day,", "a", "young", "boy", "came", "to", "Tom", "and", "Max,", "asking", "for", "their", "help.", "His", "family", "was", "in", "trouble,", "and", "he", "had", "heard", "of", "their", "bravery.", "Tom", "and", "Max", "agreed", "to", "help.", "They", "set", "off", "with", "the", "boy,", "ready", "to", "face", "another", "adventure."],
    ["The", "boy", "led", "them", "to", "a", "dark", "forest,", "where", "his", "family", "was", "trapped", "by", "a", "wicked", "sorcerer.", "Tom", "and", "Max", "confronted", "the", "sorcerer,", "using", "their", "wits", "and", "courage.", "With", "the", "help", "of", "the", "magic", "stone,", "they", "were", "able", "to", "defeat", "him", "and", "rescue", "the", "family."],
    ["Grateful,", "the", "boy's", "family", "invited", "Tom", "and", "Max", "to", "stay", "with", "them.", "They", "celebrated", "with", "a", "feast,", "sharing", "stories", "and", "laughs.", "Tom", "and", "Max", "knew", "that", "their", "adventures", "were", "far", "from", "over.", "As", "long", "as", "they", "were", "together,", "they", "could", "face", "anything."],
    ["Tom", "and", "Max", "continued", "their", "journeys,", "always", "looking", "for", "ways", "to", "help", "others.", "They", "knew", "that", "their", "friendship", "and", "bravery", "made", "them", "strong.", "Together,", "they", "traveled", "to", "new", "lands,", "faced", "new", "challenges,", "and", "made", "new", "friends.", "Their", "story", "was", "one", "of", "courage", "and", "kindness."],
    ["One", "day,", "they", "came", "across", "a", "strange", "creature", "in", "the", "woods.", "It", "was", "a", "griffin,", "majestic", "and", "fierce.", "The", "griffin", "was", "injured,", "its", "wing", "caught", "in", "a", "trap.", "Tom", "and", "Max", "carefully", "freed", "the", "griffin,", "tending", "to", "its", "wound.", "The", "griffin", "was", "grateful."],
    ["The", "griffin", "offered", "to", "help", "Tom", "and", "Max", "in", "their", "adventures.", "Together,", "they", "traveled", "to", "new", "heights,", "soaring", "above", "mountains", "and", "valleys.", "The", "griffin", "proved", "to", "be", "a", "valuable", "friend,", "using", "its", "strength", "and", "wisdom", "to", "assist", "them.", "Their", "bond", "grew", "stronger."],
    ["As", "the", "years", "went", "by,", "Tom", "knew", "his", "time", "was", "coming", "to", "an", "end.", "He", "gathered", "Max", "and", "the", "griffin,", "sharing", "his", "last", "wishes.", "He", "wanted", "them", "to", "continue", "their", "adventures,", "helping", "those", "in", "need.", "Tom", "passed", "away,", "but", "his", "legacy", "lived", "on."],
    ["Max", "and", "the", "griffin", "continued", "their", "journeys,", "honoring", "Tom's", "memory.", "They", "traveled", "far", "and", "wide,", "helping", "those", "in", "trouble,", "spreading", "kindness", "and", "courage.", "The", "stories", "of", "Tom,", "Max,", "and", "the", "griffin", "became", "legend,", "inspiring", "generations", "to", "come.", "Their", "adventures", "never", "truly", "ended."]
]

def record_audio(filename, sample_rate=44100, channels=2):
    p = pyaudio.PyAudio()

    stream = p.open(format = pyaudio.paInt16,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=512)
    
    global start 
    start = time.time()
    print("Recording...press enter to stop")
    frames = []
    try:
        while True:
            if keyboard.is_pressed('enter'):
                global end
                end = time.time()
                print("Stop recording.")
                break
            data = stream.read(512, exception_on_overflow = False)
            frames.append(data)
    except KeyboardInterrupt:
        print("Recording interrupted.")
    stream.stop_stream()
    stream.close()
    p.terminate()
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

def compare_lists(transcribed_list, correct_list):
    count = 0
    for transcribed_word, correct_word in zip_longest(transcribed_list, correct_list, fillvalue=None):
        if transcribed_word == correct_word:
            count += 1
            # print(f"Error: Expected '{correct_word}', but got '{transcribed_word}'")
    accuracy = (count/len(correct_list))
    return accuracy

# Start of Execution

iterator = 1

for sen in paragraphs:
    record_audio('recording.wav')
    model = whisper.load_model("base")
    res = model.transcribe("recording.wav")
    transcribed_text = res['text']
    print(transcribed_text.split())
    trans = transcribed_text.split()
    print("Time taken: " + str(end-start))
    speed = (len(paragraphs[0])/(end-start))*60
    accuracy = compare_lists(trans, sen)
    fluency = (speed * (accuracy))/300
    termios.tcflush(sys.stdin, termios.TCIOFLUSH)
    comfort = float(input("Enter comfort score (0 to 0.5): "))
    print("Speed: " + str(speed))
    print("Accuracy: " + str(accuracy))
    print("Fluency Score: " + str(fluency))
    print("Comfort Score: " + str(comfort))
    reward = fluency + comfort
    print("Objective Function Value for Iteration #" + str(iterator) + ": " + str(reward))
    sp.append(speed)
    acc.append(accuracy)
    flu.append(fluency)
    comf.append(comfort)
    rew.append(reward)
    
    print("Please input Objective Func Value shown above in BO.py to receive updated parameters; when ready to read with new text config, enter ""x""")
    print("")
    while True:
        if keyboard.is_pressed('x'):
            break
    termios.tcflush(sys.stdin, termios.TCIOFLUSH)
    iterator+=1    

#Overall metrics
print("Speed: ")
print(sp)
print("Accuracy: ")
print(acc)
print("Fluency: ")
print(flu)
print("Comfort: ")
print(comf)
print("Reward: ")
print(rew)
