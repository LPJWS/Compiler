; ModuleID = "/home/lpjakewolfskin/comp/compiler/codegen.py"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define void @"main"() 
{
entry:
  %"a" = alloca i8
  store i8 15, i8* %"a"
  %"b" = alloca i8
  store i8 10, i8* %"b"
  %"a.1" = load i8, i8* %"a"
  %"b.1" = load i8, i8* %"b"
  %"a.2" = load i8, i8* %"a"
  %".4" = icmp ne i8 %"a.1", %"b.1"
  br i1 %".4", label %"while", label %"while_end"
while:
  %"a.3" = load i8, i8* %"a"
  %"b.2" = load i8, i8* %"b"
  %"a.4" = load i8, i8* %"a"
  %".6" = icmp sgt i8 %"a.3", %"b.2"
  br i1 %".6", label %"while.if", label %"while.else"
while_end:
  %"a.9" = load i8, i8* %"a"
  %".16" = bitcast [5 x i8]* @"fstr" to i8*
  %".17" = call i32 (i8*, ...) @"printf"(i8* %".16", i8 %"a.9")
  ret void
while.if:
  %"a.5" = load i8, i8* %"a"
  %"b.3" = load i8, i8* %"b"
  %".8" = call i8 @"sub"(i8 %"a.5", i8 %"b.3")
  store i8 %".8", i8* %"a"
  br label %"while.endif"
while.else:
  %"b.4" = load i8, i8* %"b"
  %"a.6" = load i8, i8* %"a"
  %".11" = call i8 @"sub"(i8 %"b.4", i8 %"a.6")
  store i8 %".11", i8* %"b"
  br label %"while.endif"
while.endif:
  %"a.7" = load i8, i8* %"a"
  %"b.5" = load i8, i8* %"b"
  %"a.8" = load i8, i8* %"a"
  %".14" = icmp ne i8 %"a.7", %"b.5"
  br i1 %".14", label %"while", label %"while_end"
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

define i8 @"sub"(i8 %".1", i8 %".2") 
{
entry:
  %"res" = sub i8 %".1", %".2"
  ret i8 %"res"
}

define float @"fsub"(float %".1", float %".2") 
{
entry:
  %"res" = fsub float %".1", %".2"
  ret float %"res"
}
