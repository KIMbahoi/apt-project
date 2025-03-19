{/* <button id="raise" disabled>Raise Gate</button> */}

let port;

    // 연결 버튼 클릭 시 포트 선택 및 연결
    document.getElementById('connect').addEventListener('click', async () => {
      try {
        // 사용자가 포트를 선택하도록 요청 (HTTPS 환경에서만 작동)
        port = await navigator.serial.requestPort();
        await port.open({ baudRate: 115200 });
        document.getElementById('status').innerText = "Connected to Arduino";
        document.getElementById('raise').disabled = false;
        document.getElementById('lower').disabled = false;
      } catch (error) {
        console.error('Error connecting to serial port:', error);
        document.getElementById('status').innerText = "Connection failed";
      }
    });

    // 명령 전송 함수
    async function sendCommand(command) {
      if (!port) {
        console.error("No serial port connected");
        return;
      }
      const encoder = new TextEncoder();
      const writer = port.writable.getWriter();
      try {
        // 명령과 개행 문자 전송 (예: "RAISE\n")
        await writer.write(encoder.encode(command + "\n"));
        console.log(`Sent command: ${command}`);
      } catch (error) {
        console.error("Error writing to serial port:", error);
      } finally {
        writer.releaseLock();
      }
    }

    // 버튼 클릭 이벤트 설정
    document.getElementById('raise').addEventListener('click', () => sendCommand("RAISE"));
    document.getElementById('lower').addEventListener('click', () => sendCommand("LOWER"));