#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>


bool is_rel_primes(const int x, const int y)
{
    for (register int i = 2; i < (x > y ? y : x); ++i)
    {
        if (y % i == 0 && x % i == 0)
        {
            return false;
        }
    }

    return true;
}


int* generate_keys(const size_t n)
{
    int* keys = (int*)calloc(2, sizeof(int));

    for (register int i = 1; i < n; ++i)
    {
        for (register int j = 2; j < n; ++j)
        {
            if ((i * j) % n == 1 && is_rel_primes(i, n) && is_rel_primes(j, n))
            {
                keys[0] = i;
                keys[1] = j;
                return keys;
            }
        }
    }

    return NULL;
}


char* encrypt(const char* text, const size_t ke, const size_t n)
{
    const size_t tlength = strlen(text);
    char* result = (char*)malloc(tlength);

    for (register int i = 0; i < tlength; ++i)
    {
        result[i] = (text[i] * ke) % n;
    }

    return result;
}


char* decrypt(const char* text, const size_t kd, const size_t n)
{
    const size_t tlength = strlen(text);
    char* result = (char*)malloc(tlength);

    for (register int i = 0; i < tlength; ++i)
    {
        result[i] = (text[i] * kd) % n;
    }

    return result;
}


int main(int argc, char* argv[])
{
    const int* keys = generate_keys(256);

    if (keys == NULL)
    {
        return -1;
    }

    const int ke = keys[0];
    const int kd = keys[1];

    assert(strcmp(encrypt("cryptography", ke, 256), ")VkP\\M5V#P8k") == 0);
    assert(strcmp(decrypt(")VkP\\M5V#P8k", kd, 256), "cryptography") == 0);

    return 0;
}
