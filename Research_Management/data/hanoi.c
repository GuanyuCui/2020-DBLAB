#include <stdio.h>
void hanoi(int n, char from, char help, char to)
{
	if(n == 1)
	{
		printf("Move disk 1 from %c to %c\n", from, to);
		return;
	}
	hanoi(n - 1, from, to, help);
	printf("Move disk %d from %c to %c\n", n, from, to);
	hanoi(n - 1, help, from, to);
}
int main(int argc, char *argv[])
{
	int n;
	scanf("%d", &n);
	hanoi(n, 'a', 'b', 'c');
	return 0;
}