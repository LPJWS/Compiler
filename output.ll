; ModuleID = "/home/lpjakewolfskin/comp/compiler/codegen.py"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define void @"main"() 
{
entry:
  %".2" = call i32 @"qqq"(i32 10, i32 15)
  %"q" = alloca i32
  store i32 %".2", i32* %"q"
  %"q.1" = load i32, i32* %"q"
  %".4" = bitcast [5 x i8]* @"fstr" to i32*
  %".5" = call i32 (i32*, ...) @"printf"(i32* %".4", i32 %"q.1")
  %".6" = call i32 @"qqq"(i32 8, i32 4)
  store i32 %".6", i32* %"q"
  %"q.2" = load i32, i32* %"q"
  %".8" = bitcast [5 x i8]* @"fstr" to i32*
  %".9" = call i32 (i32*, ...) @"printf"(i32* %".8", i32 %"q.2")
  %"a" = alloca i32
  store i32 0, i32* %"a"
  %"a.1" = load i32, i32* %"a"
  %".11" = icmp sle i32 %"a.1", 10
  br i1 %".11", label %"while", label %"while_end"
while:
  %"a.2" = load i32, i32* %"a"
  %".13" = call i32 @"factor"(i32 %"a.2")
  %".14" = bitcast [5 x i8]* @"fstr" to i32*
  %".15" = call i32 (i32*, ...) @"printf"(i32* %".14", i32 %".13")
  %"a.3" = load i32, i32* %"a"
  %".16" = add i32 %"a.3", 1
  store i32 %".16", i32* %"a"
  %"a.4" = load i32, i32* %"a"
  %".18" = icmp sle i32 %"a.4", 10
  br i1 %".18", label %"while", label %"while_end"
while_end:
  %".20" = call i32 @"floor"(float 0x40179999a0000000)
  %".21" = bitcast [5 x i8]* @"fstr" to i32*
  %".22" = call i32 (i32*, ...) @"printf"(i32* %".21", i32 %".20")
  %".23" = bitcast [5 x i8]* @"fstr" to i32*
  %".24" = call i32 (i32*, ...) @"printf"(i32* %".23", i32 -5)
  ret void
}

declare i32 @"printf"(i32* %".1", ...) 

@"fstr" = internal constant [5 x i8] c"%i \0a\00"
define i32 @"sum"(i32 %".1", i32 %".2") 
{
entry:
  %"res" = add i32 %".1", %".2"
  ret i32 %"res"
}

define float @"fsum"(float %".1", float %".2") 
{
entry:
  %"res" = fadd float %".1", %".2"
  ret float %"res"
}

define i32 @"sub"(i32 %".1", i32 %".2") 
{
entry:
  %"res" = sub i32 %".1", %".2"
  ret i32 %"res"
}

define float @"fsub"(float %".1", float %".2") 
{
entry:
  %"res" = fsub float %".1", %".2"
  ret float %"res"
}

define i32 @"qqq"(i32 %".1", i32 %".2") 
{
entry:
  %"a" = alloca i32
  store i32 %".1", i32* %"a"
  %"b" = alloca i32
  store i32 %".2", i32* %"b"
  %"a.1" = load i32, i32* %"a"
  %"b.1" = load i32, i32* %"b"
  %".6" = icmp ne i32 %"a.1", %"b.1"
  br i1 %".6", label %"while", label %"while_end"
while:
  %"a.2" = load i32, i32* %"a"
  %"b.2" = load i32, i32* %"b"
  %".8" = icmp sgt i32 %"a.2", %"b.2"
  br i1 %".8", label %"while.if", label %"while.else"
while_end:
  %"a.6" = load i32, i32* %"a"
  ret i32 %"a.6"
while.if:
  %"a.3" = load i32, i32* %"a"
  %"b.3" = load i32, i32* %"b"
  %".10" = call i32 @"sub"(i32 %"a.3", i32 %"b.3")
  store i32 %".10", i32* %"a"
  br label %"while.endif"
while.else:
  %"b.4" = load i32, i32* %"b"
  %"a.4" = load i32, i32* %"a"
  %".13" = call i32 @"sub"(i32 %"b.4", i32 %"a.4")
  store i32 %".13", i32* %"b"
  br label %"while.endif"
while.endif:
  %"a.5" = load i32, i32* %"a"
  %"b.5" = load i32, i32* %"b"
  %".16" = icmp ne i32 %"a.5", %"b.5"
  br i1 %".16", label %"while", label %"while_end"
}

define i32 @"factor"(i32 %".1") 
{
entry:
  %"a" = alloca i32
  store i32 %".1", i32* %"a"
  %"res" = alloca i32
  store i32 0, i32* %"res"
  %"a.1" = load i32, i32* %"a"
  %".5" = icmp eq i32 %"a.1", 1
  %"a.2" = load i32, i32* %"a"
  %".6" = icmp eq i32 %"a.2", 0
  %".7" = or i1 %".5", %".6"
  br i1 %".7", label %"entry.if", label %"entry.else"
entry.if:
  %"a.3" = load i32, i32* %"a"
  store i32 %"a.3", i32* %"res"
  br label %"entry.endif"
entry.else:
  %"a.4" = load i32, i32* %"a"
  %".11" = sub i32 %"a.4", 1
  %".12" = call i32 @"factor"(i32 %".11")
  %"a.5" = load i32, i32* %"a"
  %".13" = mul i32 %".12", %"a.5"
  store i32 %".13", i32* %"res"
  br label %"entry.endif"
entry.endif:
  %"res.1" = load i32, i32* %"res"
  ret i32 %"res.1"
}

define i32 @"floor"(float %".1") 
{
entry:
  %"a" = alloca float
  store float %".1", float* %"a"
  %"res" = alloca i32
  store i32 0, i32* %"res"
  %"ptr" = alloca float
  store float              0x0, float* %"ptr"
  %"ptr.1" = load float, float* %"ptr"
  %"a.1" = load float, float* %"a"
  %".6" = fcmp ole float %"ptr.1", %"a.1"
  br i1 %".6", label %"while", label %"while_end"
while:
  %"res.1" = load i32, i32* %"res"
  %".8" = add i32 %"res.1", 1
  store i32 %".8", i32* %"res"
  %"ptr.2" = load float, float* %"ptr"
  %".10" = fadd float %"ptr.2", 0x3ff0000000000000
  store float %".10", float* %"ptr"
  %"ptr.3" = load float, float* %"ptr"
  %"a.2" = load float, float* %"a"
  %".12" = fcmp ole float %"ptr.3", %"a.2"
  br i1 %".12", label %"while", label %"while_end"
while_end:
  %"res.2" = load i32, i32* %"res"
  %".14" = call i32 @"sub"(i32 %"res.2", i32 1)
  ret i32 %".14"
}
