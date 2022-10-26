#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <ctype.h>


char* caesar_encryption(const char* text, const size_t key)
{
    const size_t tlength = strlen(text);
    char* result = (char*)malloc(tlength);

    for (register int i = 0; i < tlength; i++)
    {
        result[i] = (text[i] - (isupper(text[i]) == 0 ? 97 : 65) + key) % 26 + (isupper(text[i]) == 0 ? 97 : 65);
    }

    return result;
}


char* caesar_decryption(const char* text, const size_t key)
{
    const size_t tlength = strlen(text);
    char* result = (char*)malloc(tlength);

    for (register int i = 0; i < tlength; i++)
    {
        result[i] = (text[i] - (isupper(text[i]) == 0 ? 97 : 65) + 26 - key) % 26 + (isupper(text[i]) == 0 ? 97 : 65);
    }

    return result;
}


int main(int argc, char* argv[])
{
    assert(strcmp(caesar_encryption("CRYptograpHY", 3), "FUBswrjudsKB") == 0);
    assert(strcmp(caesar_decryption("FUBswrjudsKB", 3), "CRYptograpHY") == 0);
    
    return 0;
}
