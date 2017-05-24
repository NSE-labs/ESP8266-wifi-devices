import machine

ARRAYSIZE = 20

class PinToWatch:
    def __init__(self, pin_number, pull_up=False):
        self.buffer = bytearray(ARRAYSIZE)
        self.copy = bytearray(ARRAYSIZE)
        self.index = 0
        if pull_up:
            self.pin = machine.Pin(pin_number, machine.Pin.IN,
                                   machine.Pin.PULL_UP)
        else:
            self.pin = machine.Pin(pin_number, machine.Pin.IN)
        # pretend the pin changed to publish the current value
        self.pin_change(self.pin)
        self.pin.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING,
                handler=self.pin_change)

    def pin_change(self, pin):
        irq_state = machine.disable_irq()        # interrupts off
        self.buffer[self.index] = pin.value()
        self.index += 1
        if self.index >= ARRAYSIZE:
            self.index = ARRAYSIZE - 1
            print('Buffer overflow in MyDigitalPin')
        machine.enable_irq(irq_state)            # interrupts back on

    def check_pin(self, broker, topic, invert=False):
        irq_state = machine.disable_irq()        # interrupts off
        i = self.index
        for x in range(i):
            if invert:
                self.copy[x] = 1 - self.buffer[x]
            else:
                self.copy[x] = self.buffer[x]
        self.index = 0
        machine.enable_irq(irq_state)            # interrupts back on
        for x in range(i):
            broker.publish(topic, b'{}'.format(self.copy[x]))

    def publish_pin(self, broker, topic, invert=False):
        """ publish pin state regardless of whether it has changed """
        pin_state = self.pin.value()
        if invert:
            pin_state = 1 - pin_state
        broker.publish(topic, b'{}'.format(pin_state))



class PinToSample:
    def __init__(self, pin_number, pull_up=False):
        if pull_up:
            self.pin = machine.Pin(pin_number, machine.Pin.IN,
                                   machine.Pin.PULL_UP)
        else:
            self.pin = machine.Pin(pin_number, machine.Pin.IN)

    def publish_pin(self, broker, topic, invert=False):
        pin_state = self.pin.value()
        if invert:
            pin_state = 1 - pin_state
        broker.publish(topic, b'{}'.format(pin_state))
