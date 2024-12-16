#include "Buffer/StaticBuffer.h"
#include "Cache/OpenRelTable.h"
#include "Disk_Class/Disk.h"
#include "FrontendInterface/FrontendInterface.h"

#include <string.h>
#include <iostream>

void show(unsigned char buffer[])
{
  for (int i=0; i<BLOCK_SIZE; i++) 
    std::cout << (int)buffer[i] << " ";
  std::cout << "\n";
}

int main(int argc, char *argv[]) {
  
  Disk disk_run;
  // StaticBuffer buffer;
  // OpenRelTable cache;

  // unsigned char buffer[BLOCK_SIZE];   //BLOCK_SIZE is a constant that has value 2048
  // Disk::readBlock(buffer, 7000);      // 7000 is a random block number that's unused.
  // char message[] = "hello\n";
  // memcpy(buffer + 20, message, 6);    //Now, buffer[20] = 'h', buffer[21] = 'e' ...
  // Disk::writeBlock(buffer, 7000);

  // unsigned char buffer2[BLOCK_SIZE];
  // char message2[6];
  // Disk::readBlock(buffer2, 7000);
  // memcpy(message2, buffer2 + 20, 6);
  // std::cout << message2;

  unsigned char buffer [BLOCK_SIZE];
  for(int i = 0; i <= 3; i++) 
  {
    Disk::readBlock(buffer, i);
    show(buffer);
  }

  return 0;
  // return FrontendInterface::handleFrontend(argc, argv);
}