
#include <stdio.h>
int sensitive(int b, int c[])
{
    int sum = 0;
    int freeDelivery = 0;
    for (int i = 0; i < b; ++i)
    {
        sum += c[i];
    }
    printf("Order sum:%i\n", sum);
    if (sum > 100)
    {
        freeDelivery = 1;
    }
    return freeDelivery;
}

int main()
{
    int orders[] = {50, 70};
    int freeDelivery = sensitive(2, orders);
    if (freeDelivery)
    {
        printf("Your order is eligible for FREE shipping\n");
    }
    else
    {
        printf("Your order is *NOT* eligible for free shipping\n");
    }
    return 0;
}