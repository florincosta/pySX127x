from SX127x.LoRa import *
from SX127x.board_config import BOARD
from time import sleep


class MyLoRa(LoRa):

  def __init__(self, verbose=False):
    super(MyLoRa, self).__init__(verbose)
   
    self.set_mode(MODE.SLEEP)
    self.set_freq(868.0)
    self.set_modem_config_1(bw=BW.BW125, coding_rate=CODING_RATE.CR4_5)
    self.set_pa_dac(0x84)
    print str(self)

    #self.write_payload([0x0F, 0x0E, 0x04, 0x05])
    #self.set_mode(MODE.TX)
    #print str(MODE.lookup[self.get_mode()])
    #sleep(0.5)
    self.set_mode(MODE.RXCONT)

  def on_rx_done(self):
    self.clear_irq_flags(RxDone=True)
    payload = self.read_payload(nocheck=True)
    rec = ''
    for i in range(0, len(payload)):
      if payload[i] == 0:
        break;
      rec += chr(payload[i])
    print "Received payload: " + rec

def main():
  BOARD.setup()
  
  receiver = MyLoRa()

  try:
    while True:
      sleep(0.05)
      irq_flags = receiver.get_irq_flags()
      if irq_flags['rx_done'] == 1:
	receiver.on_rx_done()
 
  finally:
    BOARD.teardown()

if __name__ == "__main__":
  main()
