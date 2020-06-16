#include <stdio.h>
#include <stdlib.h>

void guardMe(void *address, const unsigned int length, const unsigned int expectedHash)
{
    const unsigned char *beginAddress = (const unsigned char *)address;
    unsigned int visited = 0;
    unsigned char hash = 0;
    while (visited < length)
    {
        hash ^= *beginAddress++;
        ++visited;
    }

    if (hash != (unsigned char)expectedHash)
    {
        printf("hash:%ui, expected:%ui", hash, expectedHash);
        exit(777);
    }
}
