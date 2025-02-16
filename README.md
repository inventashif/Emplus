# Emplus
**Task hijacking mitigation.**

**Add android:taskAffinity="" in the activity shown below. Or check the fix I have implemented in AndroidManifest.xml file then fix that in your app.(uploaded)**

![Screenshot from 2025-02-16 16-30-55](https://github.com/user-attachments/assets/c686c7c3-6e6e-4a53-b780-5c6bd9228d04)



**Optional**
1- Open your MainActivity.java (or any sensitive activity).
2- Inside the onCreate() method, paste this before setContentView():

```
@Override
protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    
    // Prevent screen overlay attacks
   ** getWindow().setFlags(WindowManager.LayoutParams.FLAG_SECURE, 
                         WindowManager.LayoutParams.FLAG_SECURE);
    **
    setContentView(R.layout.activity_main);
}
