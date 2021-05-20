; ModuleID = "C:\Users\lpjak\PycharmProjects\new_compiler2\compiler\codegen.py"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

define void @"main"() 
{
entry:
  %"a" = alloca i8
  store i8 0, i8* %"a"
  %"b" = alloca float
  store float              0x0, float* %"b"
  ret void
}

declare i32 @"printf"(i8* %".1", ...) 

@"fstr" = internal constant [5 x i8] c"%i \0a\00"
define i8 @"sum"(i8 %".1", i8 %".2") 
{
entry:
  %"res" = add i8 %".1", %".2"
  ret i8 %"res"
}

define float @"fsum"(float %".1", float %".2") 
{
entry:
  %"res" = fadd float %".1", %".2"
  ret float %"res"
}
