#include <iostream>
#include "matplotlibcpp.h"

using namespace std;
namespace plt = matplotlibcpp;

int factorial(int n)
{
    return (n == 1 || n == 0) ? 1 : factorial(n - 1) * n;
}

int main(int, char **)
{

    int n = 7;
    vector<int> x(n);
    for (int i = 0; i < n; i++)
    {
        x.at(i) = i;
    }

    vector<double> yAdd(n);
    for (int i = 0; i < n; i++)
    {
        yAdd.at(i) = 2 + i;
    }
    plt::plot(x, yAdd, "red");

    vector<double> yMultiply(n);
    for (int i = 0; i < n; i++)
    {
        yMultiply.at(i) = 2 * i;
    }
    plt::plot(x, yMultiply, "orange");

    vector<double> yExp2(n);
    for (int i = 0; i < n; i++)
    {
        yExp2.at(i) = pow(2, i);
    }
    plt::plot(x, yExp2, "yellow");

    vector<double> yExp3(n);
    for (int i = 0; i < n; i++)
    {
        yExp3.at(i) = pow(3, i);
    }
    plt::plot(x, yExp3, "green");

    vector<double> yFactorial(n);
    for (int i = 0; i < n; i++)
    {
        yFactorial.at(i) = factorial(i);
    }
    plt::plot(x, yFactorial, "blue");

    plt::show();
}
