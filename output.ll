; ModuleID = "C:\Users\lpjak\PycharmProjects\new_compiler2\compiler\codegen.py"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

define void @"main"() 
{
entry:
  %".2" = icmp slt i8 1, 2
  %".3" = xor i1 %".2", -1
  %".4" = icmp sgt i8 5, 3
  %".5" = or i1 %".3", %".4"
  br i1 %".5", label %"entry.if", label %"entry.else"
entry.if:
  %".7" = bitcast [5 x i8]* @"fstr" to i8*
  %".8" = call i32 (i8*, ...) @"printf"(i8* %".7", i8 1)
  br label %"entry.endif"
entry.else:
  br label %"entry.endif"
entry.endif:
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
