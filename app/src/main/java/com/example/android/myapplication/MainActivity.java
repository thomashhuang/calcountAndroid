package com.example.android.myapplication;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Bitmap;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;

import java.io.ByteArrayOutputStream;
import java.util.List;

public class MainActivity extends AppCompatActivity {
    private FirebaseAuth mAuth;
    private static final String TAG = "AnonymousAuth";
    private static final int CAMERA_REQUEST = 618;
    private ImageView imageView;
    TextView description;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mAuth = FirebaseAuth.getInstance();
        final MainActivity main = this;

        Button mCaptureImage = findViewById(R.id.button2);
        imageView = findViewById(R.id.image);
        description = findViewById(R.id.description);

        mAuth.signInAnonymously()
                .addOnCompleteListener(main, new OnCompleteListener<AuthResult>() {
                    @Override
                    public void onComplete(@NonNull Task<AuthResult> task) {
                        if (task.isSuccessful()) {
                            Log.d(TAG, "signInAnonymously:success");
                            FirebaseUser user = mAuth.getCurrentUser();
                        } else {
                            // If sign in fails, display a message to the user.
                            Log.w(TAG, "signInAnonymously:failure",
                                    task.getException());
                            Toast.makeText(MainActivity.this,
                                    "Authentication failed.", Toast.LENGTH_SHORT)
                                    .show();
                        }
                    }
                });

        mCaptureImage.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent cameraIntent = new Intent(android.provider.MediaStore.ACTION_IMAGE_CAPTURE);
                startActivityForResult(cameraIntent, CAMERA_REQUEST);
            }
        });
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (requestCode == CAMERA_REQUEST && resultCode == Activity.RESULT_OK) {
            Bitmap photo = (Bitmap) data.getExtras().get("data");
            imageView.setImageBitmap(photo);
            byte[] photoJPG = codec(photo, Bitmap.CompressFormat.JPEG, 80);

            try {
                ImageRecognizerAsyncTask imageRecognizerAsyncTask = new ImageRecognizerAsyncTask();
                imageRecognizerAsyncTask.execute(photoJPG);
                description.setText(getWords(imageRecognizerAsyncTask.get()));
            } catch(Exception e) {
                description.setText("failed");
            }
        }
    }

    private byte[] codec(Bitmap src, Bitmap.CompressFormat format,
                                int quality) {
        ByteArrayOutputStream os = new ByteArrayOutputStream();
        src.compress(format, quality, os);

        byte[] array = os.toByteArray();
        return array;
    }

    private String getWords(List<List<String>> description) {
        String words = "";

        for (List<String> line : description) {
            for (String word : line) {
                words += word + ", ";
            }
        }

        return words + "picture";
    }
}
