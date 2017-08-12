/*
 * gesture_control_bot.c
 *
 * Created: 12-08-2017 14:14:50
 * Author : Dhruv Srivastava
 */ 

#define F_CPU 14745600          // Crystal Frequency
#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>


unsigned char signal;			// To store received data at UDR0 from server


void init(){
	cli();						// For clearing the global interrupts
	DDRA = DDRA | 0x0F;	
	PORTA = PORTA & 0xF0;		// Motion pin refreshed
	DDRL = DDRL | 0x18;
	PORTL = PORTL | 0x18;		// Allow PWM control
	DDRC = DDRC | 0x08;		
	PORTC = PORTC & 0xF7;		// Buzzer refreshed
	UCSR0B = 0x00;				// UART0 init
	UCSR0A = 0x00;
	UCSR0C = 0x06;
	UBRR0L = 0x5F;
	UBRR0H = 0x00;
	UCSR0B = 0x98;
	sei();						// For enabling the global interrupts
}


void beep(void){
	PORTC = PINC | 0x08;        // Beep ON
	_delay_ms(100);
	PORTC = PINC & 0xF7;        // Beep OFF
}

SIGNAL(USART0_RX_vect){ 		// Reading interrupt signal values
	signal = UDR0;
	UDR0 = signal;				// Acknowledging the received signal to server
	beep();
	if(signal == 'w'){
		PORTA = 0x06;			// Forward
	}
	if(signal == 's'){
		PORTA = 0x09;			// Reverse
	}
	if(signal == 'a'){
		PORTA = 0x05;			// Left
	}
	if(signal == 'd'){
		PORTA = 0x0A;			// Right
	}
	if(signal == 'x'){
		PORTA = 0x00;			// Stop
	}
}


int main(void){
	init();
    while (1);
}
