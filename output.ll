; ModuleID = "/home/lpjakewolfskin/comp/compiler/codegen.py"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define void @"main"() 
{
entry:
  %".2" = call i8 @"qqq"(i8 10, i8 15)
  %"q" = alloca i8
  store i8 %".2", i8* %"q"
  %"q.1" = load i8, i8* %"q"
  %".4" = bitcast [5 x i8]* @"fstr" to i8*
  %".5" = call i32 (i8*, ...) @"printf"(i8* %".4", i8 %"q.1")
  %".6" = call i8 @"qqq"(i8 8, i8 4)
  store i8 %".6", i8* %"q"
  %"q.2" = load i8, i8* %"q"
  %".8" = bitcast [5 x i8]* @"fstr" to i8*
  %".9" = call i32 (i8*, ...) @"printf"(i8* %".8", i8 %"q.2")
  store i8 1, i8* %"q"
  %"q.3" = load i8, i8* %"q"
  %".11" = bitcast [5 x i8]* @"fstr" to i8*
  %".12" = call i32 (i8*, ...) @"printf"(i8* %".11", i8 %"q.3")
  %".13" = call i8 @"www"(i8 1, i8 2)
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

define i8 @"qqq"(i8 %".1", i8 %".2") 
{
entry:
  %"a" = alloca i8
  store i8 %".1", i8* %"a"
  %"b" = alloca i8
  store i8 %".2", i8* %"b"
  %"a.1" = load i8, i8* %"a"
  %"b.1" = load i8, i8* %"b"
  %".6" = icmp ne i8 %"a.1", %"b.1"
  br i1 %".6", label %"while", label %"while_end"
while:
  %"a.2" = load i8, i8* %"a"
  %"b.2" = load i8, i8* %"b"
  %".8" = icmp sgt i8 %"a.2", %"b.2"
  br i1 %".8", label %"while.if", label %"while.else"
while_end:
  %"a.6" = load i8, i8* %"a"
  ret i8 %"a.6"
while.if:
  %"a.3" = load i8, i8* %"a"
  %"b.3" = load i8, i8* %"b"
  %".10" = call i8 @"sub"(i8 %"a.3", i8 %"b.3")
  store i8 %".10", i8* %"a"
  br label %"while.endif"
while.else:
  %"b.4" = load i8, i8* %"b"
  %"a.4" = load i8, i8* %"a"
  %".13" = call i8 @"sub"(i8 %"b.4", i8 %"a.4")
  store i8 %".13", i8* %"b"
  br label %"while.endif"
while.endif:
  %"a.5" = load i8, i8* %"a"
  %"b.5" = load i8, i8* %"b"
  %".16" = icmp ne i8 %"a.5", %"b.5"
  br i1 %".16", label %"while", label %"while_end"
}

define i8 @"www"(i8 %".1", i8 %".2") 
{
entry:
  %"a" = alloca i8
  store i8 %".1", i8* %"a"
  %"b" = alloca i8
  store i8 %".2", i8* %"b"
  %"a.1" = load i8, i8* %"a"
  %"b.1" = load i8, i8* %"b"
  %".6" = add i8 %"a.1", %"b.1"
  %".7" = bitcast [5 x i8]* @"fstr" to i8*
  %".8" = call i32 (i8*, ...) @"printf"(i8* %".7", i8 %".6")
  %"a.2" = load i8, i8* %"a"
  %"b.2" = load i8, i8* %"b"
  %".9" = add i8 %"a.2", %"b.2"
  ret i8 %".9"
}
