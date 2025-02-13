# Natural Language Toolkit: Eliza
#
# Copyright (C) 2001-2023 NLTK Project
# Authors: Steven Bird <stevenbird1@gmail.com>
#          Edward Loper <edloper@gmail.com>
# URL: <https://www.nltk.org/>
# For license information, see LICENSE.TXT

# Based on an Eliza implementation by Joe Strout <joe@strout.net>,
# Jeff Epler <jepler@inetnebr.com> and Jez Higgins <mailto:jez@jezuk.co.uk>.

# Modified by Khalid M Khan
# CSC 820
# Date modified: 2/13/2024

# a translation table used to convert things you say into things the
# computer says back, e.g. "I am" --> "you are"

from newChatUtil import Chat, reflections

# a table of response pairs, where each pair consists of a
# regular expression, and a list of possible responses,
# with group-macros labelled as %1, %2.

pairs = (

    # Added 5 response pairs for the assignment CSC 820
    (
        # The course load response +ve
        # If the user express interest towards a college course
        # Eliza would try to make the user talk about the course
        # why he likes the course, or how is it differernt

        r"(.*)(like the )(.*) (courses?|classe?s?)(good)*",
        (
            "Why do you like the %3 course more than other courses?",
            "Would you like to tell me more about the %3 class?",
            "Would you like to explore more opportunities related to the field of %3?",
            "What other %4 to you like?"

        ),
    ),
    (

        # The course load response -ve
        # If the pattern detects the words class and hard/tough in the same sentence
        # Eliza would consider that the user has trouble with some subject at school
        # It would ask to user to elaborate more on this feeling
        # it would also give some recommendations to how solve this problem

        r"(.*)(courses?|classe?s?)(.*)(tough|hard|challenging)",
        (
            "There should be other courses that you like?",
            "Is it only this %2 that is %4?",
            "Do you seek help when this %2 becomes challenging??",
            "What do you think can make it better?",

        ),
    ),
    (
        # the job stress response

        # Another word that concern college students in jobs
        # as college students are continuously lookng for jobs
        # if ELIZa detects the word job/jobs

        # it would try to make the user talk about his skills
        # what work the user like to do
        # Also, ELIZA would promt the user to talk about his or her interests other than professional work
        # this could lead to talking about hobbies and passion
        r"(.*)(jobs?)",
        (
            "Are there good opportunities in the field you work in?",
            "Tell me more about your strengths and skills",
            "What things you like to work with?",
            "Do you have other passions and hobbies outside of work?",
        ),
    ),
    (
        # the AWAY FROM HOME response
        # One other problem college students may face is not feeling good because they are in a new setup
        # ELIZA would consider this patttern if the word feeling and home are used in the same input
        # it would also detect is it is usd in a negative sense

        # In reponse, ELIZA would try help the user reaching the source by talking about the reasons
        # Eliza would also give some positive ffeedback and ask questions like what makes the user feel good
        # and what places the user feels home/good
        r"(I)(.*)(not|dont)(.*)(feeling|feel)(.*)(home)(.*)",
        (
            "What are the things that make %1 feel you feel good?",
            "Is there a reason for that?",
            "What places you feel good at?",

        ),
    ),
    (
        # A food related chat response
        # Not everyone know how to cook and students generally face food problem

        # Is ELIZA specfically detects the word food
        # It would respond to explore food items user like
        # ELiza would also take the conversation a step ahead an ask about general things
        r"(.*)(food)(.*)",
        (
            "What are the food items that you like?",
            "Do you like cooking or eating out better?",
            "Are there any new places that you have discovered near the campus?"

        ),
    ),

    ##################################################################
    # ELIZA response pairs
    ##################################################################
    (
        # The need pattern
        # Pattern I need (something)

        # This pattern is very common in a therapy session
        # the user might show the desire to attain something
        # the regular expression first mathches the pattern i need something
        # In response ELIZA asks
        #             1) reason behind wanting (something)
        #             2) asking what changes would this thing bring
        #             3) ELIZA questions the users want, in a way making the user think or talk more about this need
        r"i need (.*)",
        (
            "Why do you need %1?",
            "Would it really help you to get %1?",
            "Are you sure you need %1?",
        ),
    ),
    (
        # Persepective response
        #
        # When the user tries to get confirmation from ELIZA about soemething,
        # but in a negative way by the use of the word 'dont'
        # Eliza would try to make the user understand two thing
        #           1) others opinion is not that important
        #           2) rethinking their opinion

        # Eliza would respond in way to make the user re-consider their thought

        r"whi do n\'t you (.*)",
        (
            "Do you really think I don't %1?",
            "Perhaps eventually I will %1.",
            "Do you really want me to %1?",
        ),
    ),
    (
        # Support response -ve pattern
        # Pattern - Why can't I (something)

        # This pattern is where the user express the in ablility to do something
        # In response ELIZA's repsonses would think more about this inability
        # this might lead to change users mind
        #
        # In response ELIZA says
        #             1) promotes with an idea that the user might be able to
        #             2) asking the user of the result to induce the will to do it
        #             3) Using a passing behaviour to ask the user whats stopping him,
        #             4) Giving a reality check - did you actually try it
        r"whi ca n\'t i (.*)",
        (
            "Do you think you should be able to %1?",
            "If you could %1, what would you do?",
            "I don't know -- why can't you %1?",
            "Have you really tried?",
        ),
    ),
    (
        # Assertive Negative attitude - support response
        # Pattern - I can't (something)

        # User expresses a negative attitude by stating inability to do something
        # It woudld with supportive statements to encourage
        # and consider rethinking
        # on possibilities and solutions that might help
        r"i ca n\'t (.*)",
        (
            "How do you know you can't %1?",
            "Perhaps you could %1 if you tried.",
            "What would it take for you to %1?",
        ),
    ),
    (
        # Condition/Situation response - support
        # Pattern - I am (something)

        # User describes their current condition or situation
        # ELIZA responds with supportive statements to understand the user's state
        # It also makes the user to express their feelings and thoughts about their condition

        # Asks if user's condition prompted them to seek help
        # Inquires about duration of user's condition
        # Encourages expression of user's emotions
        r"i am (.*)",
        (
            "Did you come to me because you are %1?",
            "How long have you been %1?",
            "How do you feel about being %1?",
        ),
    ),
    (
        # Condition/Situation response - want to know more!
        # Pattern - I'm (something)

        # User expresses a condition or situation they're in
        # Eliza would try to put questions that would make the user talk or elaborate on his feeling

        # it also asks about user's emotional response to their condition
        # and talk on their decision to share their condition
        r"i \'m (.*)",
        (
            "How does being %1 make you feel?",
            "Do you enjoy being %1?",
            "Why do you tell me you're %1?",
            "Why do you think you're %1?",
        ),
    ),
    (
        # Direct question - to ELIZA
        # Pattern - Are you (something)

        # User asks about ELIZA's state or attributes
        # Tries engage the user in conversation of the topic
        # and prompts the user to consider the significance of their question
        r"are you (.*)",
        (
            "Why does it matter whether I am %1?",
            "Would you prefer it if I were not %1?",
            "Perhaps you believe I am %1.",
            "I may be %1 -- what do you think?",
        ),
    ),
    (
        # Question pairs
        # Pattern - What (something)

        # User asks a question starting with "What"
        # ELIZA will try to undersatand more about user's motivation and thought process
        # encourages the user to reflect on their question and its significance
        # and prompts the user to offer other interpretations as to talk about them

        r"what (.*)",
        (
            "Why do you ask?",
            "How would an answer to that help you?",
            "What do you think?",
        ),
    ),
    (
        # Pattern - How (something)
        # It encourages the user to consider the purpose of their question
        r"how (.*)",
        (
            "How do you suppose?",
            "Perhaps you can answer your own question.",
            "What is it you're really asking?",
        ),
    ),
    (
        # Reason specific answer response
        # Pattern - Because (something)

        # User provides a reason for something
        # ELIZA responds to explore the validity of the reason
        # and prompts the user to consider additional consequences or conditions
        # This can help the user re evaluate their own idea

        r"becaus (.*)",
        (
            "Is that the real reason?",
            "What other reasons come to mind?",
            "Does that reason apply to anything else?",
            "If %1, what else must be true?",
        ),
    ),
    (
        # Apology response
        # Pattern - (anything) sorry (anything)

        # When user expresses an apology
        # ELIZA responds with inquiries to understand the user's feelings
        # it would offers reassurance and encourages the user to explore their emotions related to apologizing
        # Like a therapist it reassures the user and suggests apology may not always be necessary
        r"(.*) sorri (.*)",
        (
            "There are many times when no apology is needed.",
            "What feelings do you have when you apologize?",
        ),
    ),
    (
        # Greeting response - possibly the very first
        # Pattern - Hello(anything)

        # User initiates conversation with a greeting
        # ELIZA responds with friendly greetings and inquiries about the user's well-being
        # ELIZA aims to establish a welcoming atmosphere and engage the user in conversation
        r"hello(.*)",
        (
            "Hello... I'm glad you could drop by today.",
            "Hi there... how are you today?",
            "Hello, how are you feeling today?",
        ),
    ),
    (
        # Thought expression response
        # Pattern - I think (anything)

        # User expresses a thought or opinion
        # ELIZA responds with inquiries to explore the user's confidence in their statement
        # ELIZA prompts the user to consider their level of certainty or doubt regarding their thought
        # But it also says in a way that the user might have some more self confidence in him
        r"i think (.*)",
        ("Do you doubt %1?", "Do you really think so?", "But you're not sure %1?"),
    ),
    (
        # Friendship discussion response
        # Pattern - (anything) friend (anything)

        # User mentions the word "friend"
        # ELIZA encourage the user to talk about their friends
        # This is like starting a new comforatble conversation
        # and finding a positive memoriy related to friendship
        r"(.*) friend (.*)",
        (
            "Tell me more about your friends.",
            "When you think of a friend, what comes to mind?",
            "Why don't you tell me about a childhood friend?",
        ),
    ),
    # Affirmation response
    # Pattern - Yes

    # If the user responds with "Yes" in the query
    # ELIZA interprets the user's confidence about something
    # and shows acknowledgment
    (r"ye", ("You seem quite sure.", "OK, but can you elaborate a bit?")),
    (
        # Computer-related discussion response
        # Pattern - (anything) computer (anything)

        # User mentions the word "computer"
        # It would also check in a funny way if the user is referring to ELIZA
        # and the user is asked to express their thoughts and feelings regarding computers
        # This would be a conversation about perspective

        r"(.*) comput(.*)",
        (
            "Are you really talking about me?",
            "Does it seem strange to talk to a computer?",
            "How do computers make you feel?",
            "Do you feel threatened by computers?",
        ),
    ),
    (
        # Assumption inquiry response
        # Pattern - Is it (something)

        # User makes an assumption starting with "Is it"
        # ELIZA responds with inquiries to explore the user's thoughts
        # It also encourages user to consider their belief and gives affirmation
        # ELIZA prompts the user to consider their thoughts and actions based on the assumption
        r"is it (.*)",
        (
            "Do you think it is %1?",
            "Perhaps it's %1 -- what do you think?",
            "If it were %1, what would you do?",
            "It could well be that %1.",
        ),
    ),
    (
        # Confirmation response
        # Pattern - It is (something)

        # User expresses certainty about something
        # ELIZA responds with acknowledgments and prompts for further reflection
        # ELIZA encourages the user to consider alternative perspectives
        r"it is (.*)",
        (
            "You seem very certain.",
            "If I told you that it probably isn't %1, what would you feel?",
        ),
    ),
    (
        # Capability inquiry response
        # Pattern - Can you (something)

        # User asks if ELIZA is capable of doing something
        # It checks how the user considers ELIZA's capabilities and to talk about it
        # It may ask the user to think about the question and the intention behind it again
        r"can you (.*)",
        (
            "What makes you think I can't %1?",
            "If I could %1, then what?",
            "Why do you ask if I can %1?",
        ),
    ),
    (
        # Seeking confidence response
        # Pattern - Can I (something)

        # In situations wher the user is trying to seek confidence/approval
        # Eliza will respond in two ways, one as a challenge
        # and the other to make the user talk about the reasons and rewards about the topic in disucssion
        r"can i (.*)",
        (
            "Perhaps you don't want to %1.",
            "Do you want to be able to %1?",
            "If you could %1, would you?",
        ),
    ),
    (
        # Self-identity reflection response
        # Pattern - You are (something)

        # User makes an assumption about ELIZA's identity or characteristics
        # Eliza will turn the converastion to inquiries
        # to engage the user in self-reflection
        # It makes the user to consider their assumptions and potential projections
        r"you are (.*)",
        (
            "Why do you think I am %1?",
            "Does it please you to think that I'm %1?",
            "Perhaps you would like me to be %1.",
            "Perhaps you're really talking about yourself?",
        ),
    ),
    (

        # Pattern - You're (something)

        # When the user makes an assumption about ELIZA's identity or characteristics
        # ELIZA facilitates the user with self-reflection questions
        # and also suggests the user to consider their assumptions again
        r"you \'re (.*)",
        (
            "Why do you say I am %1?",
            "Why do you think I am %1?",
            "Are we talking about you, or me?",
        ),
    ),
    (

        # Pattern - I don't (something)

        # User expresses a negative sentiment or refusal to do something
        # the ideas here is to make the user reconsider their thoughts and desires
        # and find if any reasons behind

        r"i do n\'t (.*)",
        ("Don't you really %1?", "Why don't you %1?", "Do you want to %1?"),
    ),
    (
        # Emotional expression response
        # Pattern - I feel (something)

        # User expresses a feeling or emotion
        # tries to understand the user's emotions and experiences
        # and prompts the user to further explore and articulate their feelings
        r"i feel (.*)",
        (
            "Good, tell me more about these feelings.",
            "Do you often feel %1?",
            "When do you usually feel %1?",
            "When you feel %1, what do you do?",
        ),
    ),
    (
        # Expression of possession response
        # Pattern - I have (something)

        # User expresses ownership or possession of something
        # ELIZA tries to understand the significance and context of the user's statement
        # ask the user on their actions or plans related to the possession
        r"i have (.*)",
        (
            "Why do you tell me that you've %1?",
            "Have you really %1?",
            "Now that you have %1, what will you do next?",
        ),
    ),
    (
        # Hypothetical scenario response
        # Pattern - I would (something)

        # User expresses a hypothetical action or scenario
        # shows interest in understanding the user's motivations and intentions
        # and asks the user to elaborate more
        r"i would (.*)",
        (
            "Could you explain why you would %1?",
            "Why would you %1?",
            "Who else knows that you would %1?",
        ),
    ),
    (
        # Existence inquiry response
        # Pattern - Is there (something)

        # User asks about the existence of something
        # respond in way to to explore the user's thoughts and desires
        # and prompts the user to consider their beliefs and preferences
        # it also suggests the likelihood of the existence of the mentioned thing
        r"is there (.*)",
        (
            "Do you think there is %1?",
            "It's likely that there is %1.",
            "Would you like there to be %1?",
        ),
    ),
    (
        # Personal response
        # Pattern - My (something)

        # User expresses ownership or possession of something
        # ELIZA tries to understand the significance and context of the user's statement
        r"my (.*)",
        (
            "I see, your %1.",
            "Why do you say that your %1?",
            "When your %1, how do you feel?",
        ),
    ),
    (
        # Refocusing response
        # Pattern - You (something)

        # User directs attention or attributes something to ELIZA
        # this is to refocus the conversation back to the user
        r"you (.*)",
        (
            "We should be discussing you, not me.",
            "Why do you say that about me?",
            "Why do you care whether I %1?",
        ),
    ),
    # Inquiry response
    # Pattern - Why (something)

    # User asks "Why" about something
    # Will try to explore user's perspective behind the reason
    # Would try to dig deeper in the current feeling and keep the conversation going
    (r"whi (.*)", ("Why don't you tell me the reason why %1?", "Why do you think %1?")),
    (
        # Desire exploration response
        # Pattern - I want (something)

        # User expresses a desire or want
        # ELIZA responds with inquiries to explore the significance and motivations behind the user's desire
        # Ask the user to evaluate the implications and potential actions related to their desire
        # it also encourages the user to explain the motivations behind their desire

        r"i want (.*)",
        (
            "What would it mean to you if you got %1?",
            "Why do you want %1?",
            "What would you do if you got %1?",
            "If you got %1, then what would you do?",
        ),
    ),
    (
        # Family talk1- mother
        # Pattern - (anything) mother (anything)

        # User mentions the word "mother"
        # shows interest in user's thoughts and feelings about their mother
        # asks about relationship with their mother and its relevance to their current feelings
        r"(.*) mother(.*)",
        (
            "Tell me more about your mother.",
            "What was your relationship with your mother like?",
            "How do you feel about your mother?",
            "How does this relate to your feelings today?",
            "Good family relations are important.",
        ),
    ),
    (
        # Family Talk2 - father
        # Pattern - (anything) father (anything)

        # User mentions the word "father"
        # It helps the user understand his own relations better
        # ELIZA prompts the user to reflect on their
        #       - relationship with their father and
        # .      - its relevance to their current feelings
        r"(.*) father(.*)",
        (
            "Tell me more about your father.",
            "How did your father make you feel?",
            "How do you feel about your father?",
            "Does your relationship with your father relate to your feelings today?",
            "Do you have trouble showing affection with your family?",
        ),
    ),
    (
        # Talk about the past
        # Pattern - (anything) child(anything)

        # When the user mentions the word "child", it could mean childhood or when the user was a child situation,
        # ELIZA encourages the user to recall a positive memory from childhood
        # It responds with inquiries to explore the user's memories and experiences from childhood
        # The typing a postitive memory part will make the user experince joy from it
        # and prompts the user to reflect on their childhood experiences and how they cherlish those experieces now
        r"(.*) child(.*)",
        (
            "Did you have close friends as a child?",
            "What is your favorite childhood memory?",
            "Do you remember any dreams or nightmares from childhood?",
            "Did the other children sometimes tease you?",
            "How do you think your childhood experiences relate to your feelings today?",
        ),
    ),
    (
        # Any question query response
        # Pattern - (anything)? (ends with a question mark)

        # User asks a question
        # The user is asked to reflect on their own question
        # ELIZA encourages the user to consider finding the answer within themselves
        # Suggests that the user may already know the answer
        # Motivates the user to explore

        r"(.*)\?",
        (
            "Why do you ask that?",
            "Please consider whether you can answer your own question.",
            "Perhaps the answer lies within yourself?",
            "Why don't you tell me?",
        ),
    ),
    (
        # Exit chat query response
        # Pattern - quit

        # User indicates a desire to end the conversation
        # ELIZA responds with farewell messages
        # It may also humorously reference the idea of payment for the conversation
        # This gives a small touch to ELIZA possessing human behaviour
        r"quit",
        (
            "Thank you for talking with me.",
            "Good-bye.",
            "Thank you, that will be $150.  Have a good day!",
        ),
    ),
    (
        # Outside knowledgebase query response
        # Pattern - (anything)

        # ELIZA chooses from various make the user to provide more information
        # ELIZA may redirect the conversation or ask follow-up questions to engage the user further
        # Expresses interest in the user's input
        # Inquires about the user's emotions related to their statement
        # OR
        # Redirects the conversation to a new topic
        r"(.*)",
        (
            "Please tell me more.",
            "Let's change focus a bit... Tell me about your family.",
            "Can you elaborate on that?",
            "Why do you say that %1?",
            "I see.",
            "Very interesting.",
            "%1.",
            "I see.  And what does that tell you?",
            "How does that make you feel?",
            "How do you feel when you say that?",
        ),
    ),

)

eliza_chatbot = Chat(pairs, reflections)


def eliza_chat():
    print("Therapist\n---------")
    print("Talk to the program by typing in plain English, using normal upper-")
    print('and lower-case letters and punctuation.  Enter "quit" when done.')
    print("=" * 72)
    print("Hello.  How are you feeling today?")

    eliza_chatbot.converse()


def demo():
    eliza_chat()


if __name__ == "__main__":
    eliza_chat()