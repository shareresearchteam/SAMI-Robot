#include <Wire.h>
#include <SPI.h>
#include <Adafruit_PN532.h>




// rfid card authentication key
uint8_t keyRFID[6] = { 0xD3, 0xF7, 0xD3, 0xF7, 0xD3, 0xF7 };


// Use this line for a breakout with a hardware SPI connection.  Note that
// the PN532 SCK, MOSI, and MISO pins need to be connected to the Arduino's
// hardware SPI SCK, MOSI, and MISO pins.  On an Arduino Uno these are
// SCK = 13, MOSI = 11, MISO = 12.  The SS line can be any digital IO pin.
Adafruit_PN532 nfc(PN532_SCK, PN532_MISO, PN532_MOSI, PN532_SS);

bool initializeRFIDReader() {
  nfc.begin();

  uint32_t versiondata = nfc.getFirmwareVersion();
  if (! versiondata) {
    #if (defined(DEBUG) && DEBUG) || (defined(DEBUG_RFID) && DEBUG_RFID) 
      Serial.println("Didn't find PN53x board");
    #endif
    return false;
  }
  nfc.startPassiveTargetIDDetection(PN532_MIFARE_ISO14443A);
  return true;
}



bool verifyRFIDBlock(uint8_t block) {
  // This bit is ripped directly from the miifare classic read example
    uint8_t success;
    uint8_t uid[] = { 0, 0, 0, 0, 0, 0, 0 };  // Buffer to store the returned UID
    uint8_t uidLength;                        // Length of the UID (4 or 7 bytes depending on ISO14443A card type)
  
    // Wait for an ISO14443A type cards (Mifare, etc.).  When one is found
    // 'uid' will be populated with the UID, and uidLength will indicate
    // if the uid is 4 bytes (Mifare Classic) or 7 bytes (Mifare Ultralight)
    success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, uid, &uidLength);
  
    if (success) {
      // if we read a card...
  
      if (uidLength == 4)
      {
        // We probably have a Mifare card ...
        // So let's check the authentication of block 4
        success = nfc.mifareclassic_AuthenticateBlock (uid, uidLength, block, 0, keyRFID);
        if (success){
          // then our key worked! and everything is formatted
          return true;
          // We can go ahead and read or write!

          // If you want to write something to block 4 to test with, uncomment
    // the following line and this text should be read back in a minute
        //memcpy(data, (const uint8_t[]){ 'a', 'd', 'a', 'f', 'r', 'u', 'i', 't', '.', 'c', 'o', 'm', 0, 0, 0, 0 }, sizeof data);
        // success = nfc.mifareclassic_WriteDataBlock (4, data);

        // Try to read the contents of block 4
        //success = nfc.mifareclassic_ReadDataBlock(4, data);
        }
        else {
          // Should we try and format it?
        }
      }
      
    }
    return false;
  }

bool readRFIDBlock(uint8_t block) {
  uint8_t data[16];
  if(haveRFIDReader) {
    // first let's verify the card can be read and is correctly formatted
    if(verifyRFIDBlock(block)) {
      // Then let's try and read in our current data block
      uint8_t success = nfc.mifareclassic_ReadDataBlock(block, data);
      if(success) {
        // if we succeeded in reading it, then let's send the data!
        sendRFIDData(data);
        // then return true
        return true;
      }
    }
  }
  // Still tell the PC a card was inserted, even if we can't read it
  sendRFIDData({1});
  return false;
}

//void readRFIDCard() {
//  // If there's a card that's triggered a read
//  if(pn532Read) {
//    // Then let's read block 4 and send the data.
//    // Let's also just only use block 4
//    uint8_t success = readRFIDBlock(4);
//    // Reset our card tracker
//    pn532Read = false;
//  }
//  //nfc.startPassiveTargetIDDetection(PN532_MIFARE_ISO14443A);
//}

void checkRFIDCard() {
  if (cardTriggered) {
    #if (defined(DEBUG) && DEBUG) || (defined(DEBUG_RFID) && DEBUG_RFID) 
      Serial.println("RFID Card detector triggered");
    #endif
    // Reset the card triggered flag
    cardTriggered = false;
    // This is inverted cause the trigger pin is a pull up pin
    bool newState = !digitalRead(RFID_TRIG);
    // If the card present state is different than when we last checked, then we need to do stuff
    if(newState != cardCurrentState) {
      cardCurrentState = newState;
      if (cardCurrentState) {
        // If the new current state is high, it means we've inserted a card
        // So we should read it!
        #if (defined(DEBUG) && DEBUG) || (defined(DEBUG_RFID) && DEBUG_RFID) 
        Serial.println("Reading RFID card");
        #endif
        // Then let's read block 4 and send the data.
        // Let's also just only use block 4
        uint8_t success = readRFIDBlock(4);
      }
      else {
        // If the new current state is low, the card was removed
        #if (defined(DEBUG) && DEBUG) || (defined(DEBUG_RFID) && DEBUG_RFID) 
        Serial.println("RFID Card Removed");
      #endif
      // Send Card removed signal to pc?
      //uint8_t data[16] = {0};
      sendRFIDData({0});
      }
    }
  }
}

bool writeRFIDBlock(uint8_t data[16], uint8_t block) {
  // first let's verify the card can be read and is correctly formatted
  if(verifyRFIDBlock(block)) {
    // If we end up needing to do some weird adjustment, we can use memcpy like below:
    //    memcpy(data, (const uint8_t[]){ 'a', 'd', 'a', 'f', 'r', 'u', 'i', 't', '.', 'c', 'o', 'm', 0, 0, 0, 0 }, sizeof data);
    // Then let's try to write our data chunk to the correct block.
    uint8_t success = nfc.mifareclassic_WriteDataBlock(block, data);
    if(success) {
      return true;
    }
  }
  return false;
}
