#include <stdio.h>
#include <math.h>

int main() {
    int sine_table[1024];
    
    printf("const int sine_table[1024] = {\n");
    
    for (int i = 0; i < 1024; i++) {
        double alpha = (i / 1024.0) * (M_PI / 2.0);
        double sine_value = sin(alpha);
        sine_table[i] = (int)floor(sine_value * 32768.0);
        
        printf("    %5d", sine_table[i]);
        
        if (i < 1023) {
            printf(",");
        }
        
        if ((i + 1) % 8 == 0) {
            printf("\n");
        }
    }
    
    printf("};\n");
    
    return 0;
}
