# include <stdint.h>
# include "application.h"

#define MATMAL3  0


// CHOOSE APPLICATION HERE
#define APPLICATION MATMAL3


#define MTBAR __attribute__((section(".MTBAR_MEM")))
#define MTBDR __attribute__((section(".MTBDR_MEM")))


MTBAR void application();

MTBDR void application_entry(){
    application();
    return;
}

#if  APPLICATION == MATMAL3
    #define MAXX 10
    #define MAXY 5
    void application()
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
#endif

