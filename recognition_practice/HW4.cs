using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

// TCP stuff
using System;
using System.Threading;
using System.Net;
using System.Net.Sockets;
using System.Text;


public class HW4 : MonoBehaviour
{

    // TCP stuff
    Thread receiveThread;
    TcpClient client;
    TcpListener listener;
    int port = 9999;

    //변경할 텍스트 변수
    public TextMeshProUGUI txt_content;
    private Queue<string> queue = new Queue<string>();  //string형태의 que생성


    // Start is called before the first frame update
    void Start()
    {
        InitTCP();
    }

    // Launch TCP to receive message from python
    private void InitTCP()
    {
        receiveThread = new Thread(new ThreadStart(ReceiveData));   //새로운 thread를 만들고 데이터를 받는 메서드를 넘김.
        receiveThread.IsBackground = true;  // 생성한 thread를 백그라운드로 사용
        receiveThread.Start();
    }

    private void ReceiveData()
    {
        try
        {
            print("Waiting");
            listener = new TcpListener(IPAddress.Parse("127.0.0.1"), port); // ip주소와 포트 번호를 할당하여 TCP Listener를 생성
            listener.Start();
            Byte[] bytes = new Byte[1024];  // 클라이언트로부터 받아올 데이터의 크기를 byte로 생성

            while (true)
            {
                using (client = listener.AcceptTcpClient()) // 클라이언트 연결을 수락하고 TcpClient 객체를 반환함
                {
                    using (NetworkStream stream = client.GetStream())
                    {
                        int length;
                        while ((length = stream.Read(bytes, 0, bytes.Length)) != 0) // byte 변수에 스트림 데이터를 읽어들임. 연결이 끊어지면 0을 반환함
                        {
                            string clientMessage = Encoding.UTF8.GetString(bytes, 0, length);  //byte 형식 데이터를 UTF-8 형식으로 인코딩하고 문자열로 변환함
                            Debug.Log(clientMessage);
                            queue.Enqueue(clientMessage);   // 큐에 데이터를 저장
                            //txt_content.text= clientMessage;
                            byte [] sendData = Encoding.UTF8.GetBytes("Sending Success!");  // 문자열을 UTF-8 형식으로 인코딩하여 byte 형식으로 변환함
                            stream.Write(sendData, 0, sendData.Length);     // byte 형식 데이터를 클라이언트에 전송함
                        }
                        Debug.Log("연결이 끊어졌습니다.");
                        Debug.Log("프로세스를 종료합니다.");
                        OnApplicationQuit();
                    }
                }
            }
        }
        catch (Exception e) // 에러발생시
        {
            print(e.ToString());    //에러문 출력
        }
    }

    // Update is called once per frame
    void Update()
    {
        if(queue.Count>0){  // 큐에 데이터가 있는 경우
            txt_content.text = queue.Dequeue();    // UI 텍스트를 존재하는 데이터로 변경함
        }
    }


    void OnApplicationQuit()
    {
        // close the thread when the application quits
        receiveThread.Abort();  
    }
}