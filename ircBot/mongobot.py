import sys
import socket
import string
import time
import twitter
import ununicode

HOST="localhost"
if (sys.argv[1]):
  HOST=sys.argv[1]
print HOST
PORT=6667
NICK="MongoTwitterBot"
IDENT="mtwitbot"
REALNAME="The MongoDB Tweet Bot"
readbuffer=''
CHAN='#fun'

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
time.sleep(2)
print s.send("NICK %s\r\n" % NICK)
print s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
time.sleep(2)
print 'sent user'
time.sleep(4)
print s.send("JOIN " +CHAN + '\r\n')
time.sleep(2)
print 'sent join'
print s.send('PRIVMSG "+CHAN+" :Oh Hai.\r\n')
api = twitter.Api()

data = ''
while True:
    try:
      data = s.recv(4096)
    except:
      break

    if not data: break

    print data,
    command = data.split(' ')[1]
    print command,
    text = data.split(':')[-1]
    print text,

    print ''

    if 'PING' in command:
        print "in PING"
        s.send("PONG %s\r\n" % data.split(' ')[1])

    if 'PRIVMSG' in command:
        if 'bot' in text:
           time.sleep(1)
           s.send("PRIVMSG %s : Me too!\r\n" % CHAN)

    if 'twitter' in text:
        time.sleep(1)
        s.send('PRIVMSG %s : shush, you!\r\n' % CHAN)
    
    if 'tweet' in text:
        stati = api.GetSearch('mongodb')
        ut = [(st.user.name,st.text) for st in stati]

        print ut

        for t in ut:
           tweet = ununicode.toascii(t[1]) + '\r\n'
           print 'PRIVMSG %s :%s' % (CHAN, tweet)
           s.send('PRIVMSG %s :%s' % (CHAN, tweet))

        if len(ut) == 0:
           s.send('PRIVMSG %s : Sorry, no tweets right now!' % (CHAN))
  

    if 'bye' in data:
        s.send('PRIVMSG %s : You want me gone? \r\n' % CHAN)
        time.sleep(1)
        s.send('PRIVMSG %s : Leaving now! \r\n' % CHAN)
        s.send('PART %s : Leaving now! \r\n' % CHAN)
        time.sleep(1)
        s.send('QUIT Leaving, bye!\r\n')
        break
 
    #readbuffer=readbuffer+s.recv(1024)
    #temp=string.split(readbuffer, "\n")
    #readbuffer=temp.pop( )

s.close()
