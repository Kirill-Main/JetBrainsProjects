using System;
using System.Data.SqlTypes;
using System.Security.Principal;

namespace ConsoleApplication1
{
    internal class Program
    {
        public static void Main(string[] args)
        {
            Console.WriteLine("Привет мир!");
            
            var obj = new MySecondClass(20, "Вася");
            
            Console.WriteLine(obj.name, obj.age);
        }
    }

    internal class MyClass
    {
        public string name;

        public MyClass(string name="")
        {
            this.name = name;
        }
        
    }

    internal class MySecondClass : MyClass
    {
        public int age;
        
        public MySecondClass(int age, string name = "")
            : base(name)
        {
            this.age = age;
        }
    }
}