#include <stdlib.h>
#include <string.h>
#include <assert.h>


char* encrypt(const char* text, const size_t k, const size_t n)
{
    const size_t tlength = strlen(text);
    char* result = (char*)malloc(tlength);

    for (register int i = 0; i < tlength; ++i)
    {
        result[i] = (text[i] + k) % n;
    }

    return result;
}


char* decrypt(const char* text, const size_t k, const size_t n)
{
    const size_t tlength = strlen(text);
    char* result = (char*)malloc(tlength);

    for (register int i = 0; i < tlength; ++i)
    {
        result[i] = (text[i] + n - k) % n;
    }

    return result;
}


int main(int argc, char* argv[])
{
    assert(strcmp(encrypt("cryptography", 3, 256), "fu|swrjudsk|") == 0);
    assert(strcmp(decrypt("fu|swrjudsk|", 3, 256), "cryptography") == 0);
    return 0;
}
