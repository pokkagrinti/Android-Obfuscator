.class public Lcom/example/week8lab/MainActivity;
.super Landroidx/appcompat/app/AppCompatActivity;
.source "MainActivity.java"


# direct methods
.method public constructor <init>()V
    .locals 1


    const v0, 0
    :obfus_loop
    packed-switch v0, :pswitch_obf

    :obf_pswitch_0

    .line 7
    invoke-direct {p0}, Landroidx/appcompat/app/AppCompatActivity;-><init>()V

    return-void
    :goto obfus_loop

    :pswitch_obf
    .packed-switch 0x0
        :obf_pswitch_0
    .end packed-switch

.end method.method public fun(I)I
    .locals 7
	
    const-string v0, "MYINT"

    const-string v1, "cansee?"



    const v6, 0
    :obfus_loop
    packed-switch v6, :pswitch_obf

    :obf_pswitch_0

    .line 20
    invoke-static {v0, v1}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I

    const/4 v1, 0x0

    const/4 v2, 0x0

    const/4 v3, 0x0

    :goto_0
    if-ge v2, p1, :cond_1

    const/4 v4, 0x0

    :goto_1
    if-ge v4, p1, :cond_0

    add-int/2addr v3, v4

    const-string v5, "HELLO"

    const v6, 1
    :goto obfus_loop

    :obf_pswitch_1

    .line 26
    invoke-static {v5, v5}, Landroid/util/Log;->v(Ljava/lang/String;Ljava/lang/String;)I

    add-int/lit8 v4, v4, 0x1

    goto :goto_1

    :cond_0
    add-int/lit8 v2, v2, 0x1

    goto :goto_0

    :cond_1
    const-string p1, "cansee2?"

    const v6, 2
    :goto obfus_loop

    :obf_pswitch_2

    .line 32
    invoke-static {v0, p1}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I

    const-string p1, "overwrite?"

    const v6, 3
    :goto obfus_loop

    :obf_pswitch_3

    .line 33
    invoke-static {v0, p1}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I

    return v3
    :goto obfus_loop

    :pswitch_obf
    .packed-switch 0x0
        :obf_pswitch_0
        :obf_pswitch_1
        :obf_pswitch_2
        :obf_pswitch_3
    .end packed-switch

.end method.method protected onCreate(Landroid/os/Bundle;)V
    .locals 3


    const v2, 0
    :obfus_loop
    packed-switch v2, :pswitch_obf

    :obf_pswitch_0

    .line 11
    invoke-super {p0, p1}, Landroidx/appcompat/app/AppCompatActivity;->onCreate(Landroid/os/Bundle;)V

    const p1, 0x7f0b001c

    const v2, 1
    :goto obfus_loop

    :obf_pswitch_1

    .line 12
    invoke-virtual {p0, p1}, Lcom/example/week8lab/MainActivity;->setContentView(I)V

    const/16 p1, 0xa

    const v2, 3
    :goto obfus_loop

    :obf_pswitch_2

    .line 15
    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    const-string v1, "value: "

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0, p1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    const-string v0, "MYINT"

    invoke-static {v0, p1}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I

    return-void
    :goto obfus_loop

    :obf_pswitch_3

    .line 14
    invoke-virtual {p0, p1}, Lcom/example/week8lab/MainActivity;->fun(I)I

    move-result p1

    const v2, 2
    :goto obfus_loop

    :pswitch_obf
    .packed-switch 0x0
        :obf_pswitch_0
        :obf_pswitch_1
        :obf_pswitch_2
        :obf_pswitch_3
    .end packed-switch

.end method