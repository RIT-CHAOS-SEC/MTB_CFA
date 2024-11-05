# include <stdint.h>
# include "application.h"

#define MAXX 10
#define MAXY 5
__attribute__((section(".MTBDR_MEM"))) void matmul3()
{
    int mat[MAXX][MAXY];
    int val = 0;
    if (val == 1)
    {
        val++;
    }
    else
    {
        val += 4;
    }

    for (int x = 0; x < MAXX; x++)
    {
        for (int y = 0; y < MAXY; y++)
        {
            val += mat[x][y] + mat[y][x];
        }
    }
    val = val + 2;
    return;
}


__attribute__((section(".MTBAR_MEM"))) void matmul3_entry(){
    matmul3();
    return;
}