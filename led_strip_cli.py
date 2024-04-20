import zmq
import sys
import config

# Init ZMQ client.
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect('tcp://localhost:' + str(config.ZMQ_PORT))

# Fetch input arguments.
cmd = 'cmd'
if(len(sys.argv) == 2):
    cmd = sys.argv[1]
    # Send ZMQ request.
    socket.send(cmd.encode('utf-8'))
else:
    print('Usage:\n\t' + __file__ + ' <cmd>\ncmd:')
    print('\tlntr_on : activate lantern mode.'    )
    print('\tlntr_off: deactivate lantern mode.'  )
    print('\ttmlp_on : activate timelapse mode.'  )
    print('\ttmlp_off: deactivate timelapse mode.')
    print('\tprog_on : activate progress mode.'   )
    print('\tprog_off: deactivate progress mode.' )
    print('\tfail_on : activate fail mode.'       )
    print('\tfail_off: deactivate fail mode.'     )
    print('')
