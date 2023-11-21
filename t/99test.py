#!/bin/env python3
'''
     Title: 01test
 Copyright: Copyright 2023 by Shawn H Corey. Some rights reserved.
   Purpose: Test the Field Sort for the Zinm Desktop Wiki.

   Licence: This file is part of Field Sort.

            Field Sort is free software: you can
            redistribute it and/or modify it under the terms of
            the GNU General Public License as published by the
            Free Software Foundation, either version 3 of the
            License, or (at your option) any later version.

            Field Sort is distributed in the hope that
            it will be useful, but WITHOUT ANY WARRANTY; without
            even the implied warranty of MERCHANTABILITY or
            FITNESS FOR A PARTICULAR PURPOSE. See the GNU
            General Public License for more details.

            You should have received a copy of the GNU General
            Public License along with Field Sort.
            If not, see <https://www.gnu.org/licenses/>.
'''

import subprocess
import os
import re

cwd = os.path.dirname(os.path.realpath(__file__))
field_sort = cwd + "/../field_sort.py"

marked = """* "Space is big. Really big. You just won't believe how vastly, hugely, mind-bogglingly big it is. I mean, you may think it's a long way down the road to the chemist, but that's just peanuts to space." — __Douglas__ __Adams__, The Hitchhiker's Guide to the Galaxy
* "Don't panic." — __Douglas__ __Adams__, The Hitchhiker's Guide to the Galaxy
* "In the beginning the Universe was created. This has made a lot of people very angry and has been widely regarded as a bad move." — __Douglas__ __Adams__
* "In those days spirits were brave, the stakes were high, men were real men, women were real women and small furry creatures from Alpha Centauri were real small furry creatures from Alpha Centauri." — __Douglas__ __Adams__
* "It is a mistake to think you can solve any major problem just with potatoes." — __Douglas__ __Adams__
* "There is a theory which states that if ever anybody discovers exactly what the Universe is for and why it is here, it will instantly disappear and be replaced by something even more bizarre and inexplicable. There is another theory which states that this has already happened." — __Douglas__ __Adams__
* "No one is as arrogant as a beginner." — __Elizabeth__ __Ashley__
* "Anti-intellectualism has been a constant thread winding its way through our political and cultural life, nurtured by the false notion that democracy means that 'my ignorance is just as good as your knowledge.'" — __Isaac__ __Asimov__
* "On two occasions I have been asked [by members of Parliament], "Pray, Mr. Babbage, if you put into the machine wrong figures, will the right answers come out?" I am not able rightly to apprehend the kind of confusion of ideas that should provoke such a question." — __Charles__ __Babbage__
* "Any fool can write code that a computer can understand. Good programmers write code that humans can understand." — __Kent__ __Beck__
* "A big piece of the story we tell ourselves about who we are, is that we are willing to invent. We are willing to think long-term. We start with the customer and work backwards. And, very importantly, we are willing to be misunderstood for long periods of time." — __Jeff__ __Bezos__, Amazon's CEO
* "We are stubborn on vision. We are flexible on details... We don’t give up on things easily." — __Jeff__ __Bezos__, Amazon's CEO
* "An expert is a person who has made all the mistakes that can be made in a very narrow field." — __Niels__ __Bohr__
* "Documentation is like sex: when it's good, it's very, very good; and when it's bad, it's still better than nothing." — __Dick__ __Brandon__
* "Show me your flowchart and conceal your tables, and I shall continue to be mystified. Show me your tables, and I won't usually need your flowchart; it'll be obvious." — __Fred__ __Brooks__, The Mythical Man-month
* "The management question, therefore, is not whether to build a pilot system and throw it away. You will do that. […] Hence plan to throw one away; you will, anyhow." — __Fred__ __Brooks__, The Mythical Man-month
* "If you want to teach people a new way of thinking, don't bother trying to teach them. Instead, give them a tool, the use of which will lead to new ways of thinking." — __Richard__ __Buckminster Fuller__
* "Any day you get to keep all your limbs is a good day." — __Jack__ __Candle__, Order of the Stick forums
* "Always code as if the guy who ends up maintaining, or testing your code will be a violent psychopath who knows where you live." — __Dave__ __Carhart__
* "A good novel tells us the truth about its hero; but a bad novel tells us the truth about its author." — __G.K.__ __Chesterton__
* "Success is the ability to go from one failure to another with no loss of enthusiasm." — __Winston__ __Churchill__
* "We make a living by what we get, we make a life by what we give." — __Winston__ __Churchill__
* "Inspiration usually arrives at the keyboard at about the same time we do." — __Robert Chazz__ __Chute__
* "You can never make the same mistake twice because the second time you make it, it's not a mistake, it's a choice" —  __Steven__ __Denn__
* “Perfection is achieved, not when there is nothing more to add, but when there is nothing left to take away.” — __Antoine__ __de Saint-Exupéry__, Airman's Odyssey
* "Our imagination is nothing compared with nature's reality." — __Neil__ __deGrasse Tyson__
* "Every pirate wants to be an admiral." — __Cory__ __Doctorow__, http://craphound.com/?p=3510
* "For me — for pretty much every writer — the big problem isn't piracy, it's obscurity (thanks to Tim O'Reilly for this great aphorism)." — __Cory__ __Doctorow__, http://craphound.com/littlebrother/about/
* "Any intelligent fool can make things bigger and more complex... It takes a touch of genius - and a lot of courage to move in the opposite direction." — __Albert__ __Einstein__
* "I am thankful to all those who said no. It's because of them, I did it myself." — __Albert__ __Einstein__
* "If at first, the idea is not absurd, then there is no hope for it." — __Albert__ __Einstein__
* "If we knew what it was we were doing, it would not be called research, would it?" — __Albert__ __Einstein__
* "If you can't explain it simply, you don't understand it well enough." — __Albert__ __Einstein__
* "Only two things are infinite, the universe and human stupidity, and I'm not sure about the former." — __Albert__ __Einstein__
* "The difference between genius and stupidity is that genius has its limits." — __Albert__ __Einstein__
* "The world is a dangerous place to live; not because of the people who are evil, but because of the people who don't do anything about it." — __Albert__ __Einstein__
* "Those who have the privilege to know, have the duty to act." — __Albert__ __Einstein__
* "Truth is what stands the test of experience." — __Albert__ __Einstein__
* "When we all think alike, no one thinks very much." — __Albert__ __Einstein__
* "The only thing worth writing about is the human heart in conflict with itself." — __William__ __Faulkner__
* "Anyone who claims to understand quantum theory is either lying or crazy." — __Richard__ __Feynman__
* "If I could explain it [quantum electrodynamics] to the average person, it wouldn't have been worth the Nobel prize." — __Richard__ __Feynman__
* "Once is happenstance. Twice is coincidence. Three times is enemy action." — __Ian__ __Fleming__, Goldfinger
* "The owner, the employees, and the buying public are all one and the same, and unless an industry can so manage itself as to keep wages high and prices low it destroys itself, for otherwise it limits the number of its customers. One’s own employees ought to be one’s own best customers. We increased the buying power of our own people, and they increased the buying power of other people, and so on and on. It is this thought of enlarging buying power by paying high wages and selling at low prices that is behind the prosperity of this country." — __Henry__ __Ford__, Today and Tomorrow
* "We are all born ignorant, but one must work hard to remain stupid." — __Benjamin__ __Franklin__
* "For success, like happiness, cannot be pursued; it must ensued, and it only does so as the unintended consequence of one’s personal dedication to a cause greater than oneself..." — __Viktor__ __Frankl__, Man’s Search for Meaning
* "Large systems that work start as small systems that work." — __John__ __Gall__, Systemantics
* "Earth provides enough to satisfy every man's needs, but not every man's greed." — __Mohandas Karamchand__ __Gandhi__
* "When asked what he thought of civilization, Mahatma Gandhi replied, "Yes, it would be nice."" — __Mohandas Karamchand__ __Gandhi__
* "You can't pull yourself up by your bootstraps if you have no boots." — __Joseph__ __Hanlon__
* "Write drunk, edit sober." — __Ernest__ __Hemingway__
* "Write sober, edit drunk." — __Ernest__ __Hemingway__
* "They [science-fiction authors] scarcely imagined the actual situation of three or four decades later, when a rocket costing perhaps $100 million would lift off, perform a mission, and be destroyed either by falling into the ocean or by burning up reentering the atmosphere. Arthur Clarke said of those days, "We were not that imaginative."" — __T.A.__ __Heppenheimer__, Colonies in Space
* "Everything is under control." — __Peter__ __Jackson__
* "Pain is temporary, film is forever." — __Peter__ __Jackson__
* "The purpose of a song isn't just to show off your skills, go through the riffs and croons, it's to transmit emotion to the audience." — __Randy__ __Jackson__, American Idol
* "If you need root access to do your job, it is a bug." — __Elizabeth Krumbach__ __Joseph__
* "Technology is only technology to people born before it was invented." — __Alan__ __Kay__
* "I will mourn the loss of thousands of precious lives, but I will not rejoice in the death of one, not even an enemy. Returning hate for hate multiplies hate, adding deeper darkness to a night already devoid of stars. Darkness cannot drive out darkness; only light can do that. Hate cannot drive out hate, only love can do that." — __Martin Luther__ __King__ Jr., Strength to Love
* "Beware of bugs in the above code - I have only proven it correct, not tested it." — __Don__ __Knuth__
* "The word is not the thing. The map is not the territory. The symbol is not the thing symbolized." — __Alfred__ __Korzybski__
* "A weak man has doubts before a decision, a strong man has them afterwards." — __Karl__ __Kraus__, Austrian author and journalist (1874 -1936)
* "Anything designed with being inoffensive as its primary goal isn't going to be worth your time — life itself is pretty offensive, ending as it does with death." — __Holly__ __Lisle__
* "The power of one, if fearless and focused, is formidable, but the power of many working together is better." — __Gloria Macapagal__ __Arroyo__
* "Please accept my resignation. I don't want to belong to any club that will accept people like me as a member." — __Groucho__ __Marx__
* "Once you stop the painting, and show it to somebody else, it no longer belongs to you." — __Dave__ __Mathews__
* "Fascism should more properly be called corporatism because it is the merger of state and corporate power." — __Benito__ __Mussolini__
* "You know, I have one simple request. And that is to have sharks with frickin' laser beams attached to their heads!" — __Mike "Dr. Evil"__ __Myers__
* "Dignity is more important to the human spirit than wealth." — __Jacqueline__ __Novogratz__
* "The markets alone will not solve the problems of poverty." — __Jacqueline__ __Novogratz__
* "Traditional charity and aid alone will not solve the problems of poverty." — __Jacqueline__ __Novogratz__
* "Never grow a wishbone, daughter, where your backbone ought to be." — __Clementine__ __Paddleford__
* "Okay, class. Optical orbits up front, and remember, we keep our subesophageal ganglion to ourselves." — __Bob "Mr. Ray"__ __Peterson__, Finding Nemo
* "Smart data structures and dumb code works a lot better than the other way around." — __Eric S.__ __Raymond__, The Cathedral and the Bazaar
* "To boldly go where no-one has gone before." — __Eugene Wesley "Gene"__ __Roddenberry__, Star Trek
* "Only thing we have to fear is fear itself." — __Franklin D.__ __Roosevelt__, First Inaugural Address
* "It takes grace to remain kind, in cruel situations." — __Rupi__ __Kaur__
* "Perl is the duck tape of the Internet." — __Hassan__ __Schroeder__, Sun's first webmaster
* "The secret to happiness is low expectations." — __Barry__ __Schwartz__
* "Why fit in when you can stand out?" — __Theodor__ __Seuss "Dr. Seuss" Geisel__
* "What's in a name? That which we call a rose, By any other name would smell as sweet." — __William__ __Shakespeare__, Romeo and Juliet
* "There are more things in heaven and earth, Horatio, Than are dreamt of in your philosophy." — __William__ __Shakespeare__, Hamlet
* "Democracy is a device that insures we shall be governed no better than we deserve." — __George Bernard__ __Shaw__
* "Be generous with the duck tape. You know: spare the duck tape, spoil the job." — __Steve "Red Green"__ __Smith__
* "There's only two things that excite a man: expensive toys and real expensive toys." — __Steve "Red Green"__ __Smith__
* "To me, cheating just means you care about winning." — __Steve "Red Green"__ __Smith__
* "VEGETARIAN: That's an old Indian word meaning 'I don't hunt so good.'" — __Steve "Red Green"__ __Smith__
* "You can't stay young but you can stay immature." — __Steve "Red Green"__ __Smith__
* "Quantity has a quality all its own." — __Joseph Vissarionovich__ __Stalin__
* "I have always wished that my computer would be as easy to use as my telephone. My wish has come true. I no longer know how to use my telephone." — __Bjarne__ __Stroustrup__
* "Creativity isn’t about wild talent as much as it’s about productivity. To find new ideas that work, you need to try a lot that don’t. It’s a pure numbers game." — __Robert__ __Sutton__
* "Are we not part of this world? Tell me mellon, when did we let evil grow stronger than us?" — __Tauriel__, The Delosation of Smaug
* "Make something worthwhile." — __The__ __Dear Hunter__
* "'It needs but one foe to breed a war, not two, Master Warden,' answered Éowyn. 'And those who have not swords can still die upon them." — __J.R.R.__ __Tolkien__, The Lord of the Rings
* "All that is gold does not glitter; not all those that wander are lost." — __J.R.R.__ __Tolkien__, The Lord of the Rings
* "All we have to decide is what to do with the time that is given to us." — __J.R.R.__ __Tolkien__, The Lord of the Rings
* "Gildor was silent for a moment. 'I do not like this news,' he said at last. 'That Gandalf should be late, does not bode well. But it is said: Do not meddle in the affairs of Wizards, for they are subtle and quick to anger. The choice is yours: to go or wait.' 'And it is also said,' answered Frodo: 'Go not to the Elves for counsel, for they will say both no and yes.' 'Is it indeed?' laughed Gildor. 'Elves seldom give unguarded advice, for advice is a dangerous gift, even from the wise to the wise, and all courses may run ill.'" — __J.R.R.__ __Tolkien__, The Lord of the Rings
* "I don't know half of you half as well as I should like; and I like less than half of you half as well as you deserve." — __J.R.R.__ __Tolkien__, The Lord of the Rings
* "If more of us valued food and cheer and song above hoarded gold, it would be a merrier world." — __J.R.R.__ __Tolkien__
* "It's a dangerous business going out your front door." — __J.R.R.__ __Tolkien__, The Lord of the Rings
* "It's a job that's never started that takes the longest to finish." — __J.R.R.__ __Tolkien__
* "Many that live deserve death. And some die that deserve life. Can you give it to them? Then be not too eager to deal out death in the name of justice, fearing for your own safety. Even the wise cannot see all ends." — __J.R.R.__ __Tolkien__, The Lord of the Rings
* "There is nothing like looking, if you want to find something. You certainly usually find something, if you look, but it is not always quite the something you were after." — __J.R.R.__ __Tolkien__, The Hobbit
* "The only way that problems get solved in real life is with a lot of hard work on getting the details right." — __Linus__ __Torvalds__
* "The report of my death was an exaggeration." — __Mark__ __Twain__
* "Few things are harder to put up with than the annoyance of a good example." — __Mark__ __Twain__, Pudd'nhead Wilson (1894)
* "I don't give a damn for a man that can only spell a word one way." — __Mark__ __Twain__
* "I was gratified to be able to answer promptly. I said I don't know." — __Mark__ __Twain__
* "If you tell the truth you don't have to remember anything." — __Mark__ __Twain__
* "It is better to keep your mouth closed and let people think you are a fool than to open it and remove all doubt." — __Mark__ __Twain__
* "Keep away from people who try to belittle your ambitions. Small people always do that, but the really great make you feel that you, too, can become great." — __Mark__ __Twain__
* "Let us be thankful for the fools. But for them the rest of us could not succeed." — __Mark__ __Twain__
* "Let us so live that when we come to die even the undertaker will be sorry." — __Mark__ __Twain__
* "Never put off until tomorrow what you can do the day after tomorrow." — __Mark__ __Twain__
* "The best way to cheer yourself is to try to cheer someone else up." — __Mark__ __Twain__
* (circa 1960) "It would appear that we have reached the limits of what it is possible to achieve with computer technology, although one should be careful with such statements, as they tend to sound pretty silly in 5 years."" — __John__ __von Neumann__
* "If you want your life to be more rewarding, you have to change the way you think." — __Oprah__ __Winfrey__, O Magazine
* "The biggest adventure you can ever take is to live the life of your dreams." — __Oprah__ __Winfrey__, O Magazine


"""

lines = re.sub('__', '', marked)

status = subprocess.call([field_sort, marked, lines])
print("\n")
if status == 0:
    print("sort initiated")
else:
    print(f"sort cancelled: {status}")
