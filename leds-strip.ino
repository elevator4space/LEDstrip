#include <avr/wdt.h>
#include <Console.h>
#include <FastLED.h>
#include <stdio.h>
#include <string.h>

#define NUM_LEDS 150
#define DATA_PIN 2
#define CLOCK_PIN 13

CRGB leds[NUM_LEDS];
String input_buffer;
String command[3];

void setup()
{
	wdt_enable(WDTO_4S);
	Serial.begin(9600);
    FastLED.addLeds<WS2812B, DATA_PIN, RGB>(leds, NUM_LEDS);
	Serial.println("Welcome to LEDs STRIP");
	Serial.println(".. by Space Elevator");
	Serial.println("\nEnter command: ");
	wdt_reset();
}

void setAllColor(CRGB Color) {
  	for(int i = 0; i < NUM_LEDS; i++) {
      leds[i] = Color;
    }
    FastLED.show();
}

int StringSplit(String sInput, char cDelim, String sParams[], int iMaxParams)
{
    int iParamCount = 0;
    int iPosDelim, iPosStart = 0;

    do {
        // Searching the delimiter using indexOf()
        iPosDelim = sInput.indexOf(cDelim,iPosStart);

        if (iPosDelim >= (iPosStart+1)) {
            // Adding a new parameter using substring() 
            sParams[iParamCount] = sInput.substring(iPosStart,iPosDelim);
            iParamCount++;
            // Checking the number of parameters
            if (iParamCount >= iMaxParams) {
                return (iParamCount);
            }
            iPosStart = iPosDelim + 1;
        }
    } while (iPosDelim >= 0);
    if (iParamCount < iMaxParams) {
        // Adding the last parameter as the end of the line
        sParams[iParamCount] = sInput.substring(iPosStart);
        iParamCount++;
    }

    return (iParamCount);
}

void loop() {

  if (Serial.available() > 0) {
	wdt_reset();
	char c = Serial.read();
	Serial.print(c);

	if (c == ';') {
		Serial.println("Received.");
		StringSplit(input_buffer, ',', command, 3);
		Serial.println(command[0]);
		Serial.println(command[1]);
		Serial.println(command[2]);
		setAllColor(CRGB(command[1].toInt(), command[0].toInt(), command[2].toInt())); // Two first params inversed (GRB to RGB) because the strip is badly coded
		wdt_reset();
    	input_buffer = "";
		Serial.println("Enter command: ");
    }
	else {
      input_buffer += c;
    }
  } else {
    delay(100);
	wdt_reset();
  }
}
