package com.example.growth4;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import android.content.DialogInterface;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageButton;
import android.widget.Toast;
import android.util.Log;

import com.google.firebase.iid.FirebaseInstanceId;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        String test = FirebaseInstanceId.getInstance().getToken();
        Log.d("Token Value", test);

        //cctv 실시간 스트리밍으로 넘어감
        ImageButton camerastreaming = (ImageButton) findViewById(R.id.camerastreaming);
        camerastreaming.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(getApplicationContext(), CameraStreaming.class);
                startActivityForResult(intent, 101);
            }
        });


        //기록으로 넘어감
        ImageButton log = (ImageButton) findViewById(R.id.visitorlog);
        log.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(getApplicationContext(), Visitor.class);
                startActivityForResult(intent, 103);
            }
        });

        //비상연락버튼을 눌렀을 때 팝업
        ImageButton siren = (ImageButton) findViewById(R.id.siren);
        siren.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                showPopup();
            }
        });
    }

    //비상연락 팝업, 예 누르면 112로 연결, 아니오 누르면 뒤로가기
    void showPopup() {
        AlertDialog.Builder msgBuilder = new AlertDialog.Builder(MainActivity.this)
                .setTitle("112로 연결하겠습니까?")
                .setMessage("확인을 누르면 즉시 112로 연결됩니다")
                .setPositiveButton("확인", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialogInterface, int i) {
                        Intent intent = new Intent(Intent.ACTION_VIEW);
                        intent.setData(Uri.parse("tel:112"));
                        startActivity(intent);

                        try{
                            startActivity(intent);
                        }catch(Exception e) {
                            e.printStackTrace();
                        }
                    }
                })
                .setNegativeButton("뒤로", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialogInterface, int i) {
                        Toast.makeText(MainActivity.this, "112 연결을 취소했습니다.", Toast.LENGTH_SHORT).show();
                    }
                });
        AlertDialog msgDlg = msgBuilder.create();
        msgDlg.show();
    }
}