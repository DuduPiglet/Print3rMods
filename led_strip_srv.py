import zmq
import time
import config
import lib.LedStrip.LedStrip as ls

# Initialize ZMQ socket.
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind('tcp://*:' + str(config.ZMQ_PORT))

def __lntrOn(ledStrip):
    ledStrip.SetModeEn('lntr', True)

def __lntrOff(ledStrip):
    ledStrip.SetModeEn('lntr', False)

def __tmlpOn(ledStrip):
    ledStrip.SetModeEn('tmlp', True)

def __tmlpOff(ledStrip):
    ledStrip.SetModeEn('tmlp', False)

def __progOn(ledStrip):
    ledStrip.SetModeEn('prog', True)

def __progOff(ledStrip):
    ledStrip.SetModeEn('prog', False)

def __failOn(ledStrip):
    ledStrip.SetModeEn('fail', True)

def __failOff(ledStrip):
    ledStrip.SetModeEn('fail', False)

dispatch = {
    'lntr_on' : __lntrOn,
    'lntr_off': __lntrOff,
    'tmlp_on' : __tmlpOn,
    'tmlp_off': __tmlpOff,
    'prog_on' : __progOn,
    'prog_off': __progOff,
    'fail_on' : __failOn,
    'fail_off': __failOff,
}

ledStrip = ls.LedStrip(len=config.LED_STRIP_LENGTH, pin=config.LED_STRIP_PIN)
ledStrip.SetModeEn('init', True)
ledStrip.SetColorConf('init', 255, 255, 255, 1  )
ledStrip.SetColorConf('lntr', 255, 255, 255, 1  )
ledStrip.SetColorConf('tmlp', 255, 255, 255, 1  )
ledStrip.SetColorConf('prog', 0,   255, 0,   0.2)
ledStrip.SetColorConf('fail', 255, 0,   0,   0.2)

def digestMsg(ledStrip, msg):
    response = 'nok'
    if msg in dispatch:
        dispatch[msg](ledStrip)
        response = 'ok'
    socket.send(response.encode('utf-8'))

while True:
    try:
        digestMsg(ledStrip, socket.recv(flags=zmq.NOBLOCK).decode('utf-8'))
    except zmq.Again as e:
        pass
    ledStrip.Process()
    time.sleep(0.005)
