import serial

class signalling(object):
    def __init__(self,port,baud):
        self.last = None        # References the last captured signal
        self.curr = None        # References the current active signal sent to bot
        self.ack = None         # Captures the acknowledged symbol from the bot.
        self.counter = 0        # Counter to match last 4 symbols.
        self.port = port        # Port at which transmitter is connected to server.
        self.baud = baud        # Speed of communication between transmitter and reciever.
        self.ser = serial.Serial(self.port,self.baud, timeout=1)

    def send(self,signal):
        """
        Controls the signals sent to robot.
        - Avoids repettive signalling.
        - Checks previous 4 signals to avoid false predictions during gesture transitions.
        - Keeps sending the signal to Bot until acknowledgment is received.
        """
        if signal==self.curr or self.counter>4:
            pass
        elif signal==self.last:
            self.counter += 1
            if self.counter==4:
                self.curr = signal
                while(self.ack is None):
                    self.ser.write(self.curr.encode('ascii'))
                    self.ack = str(self.ser.read(1).decode('ascii'))
                    print('received', self.ack)
                self.ack = None
        else:
            self.counter = 0
        self.last = signal

