# test.py

import os
import sys

# 이 파일이 있는 폴더를 import 경로 맨 앞에 추가하여 로컬 모듈을 불러옵니다.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tcp import connect_one, connect_with_fallback
from dns import resolve
from http import build_request, send_and_recv, parse_status_and_preview


def test_http():
    print("=" * 60)
    print("HTTP 로직 테스트 (http.py)")
    print("=" * 60)
    print()

    # 테스트 7: build_request - HTTP/1.1 요청 메시지 형식 검증
    print("--- [테스트 7: build_request 형식] ---")
    req = build_request("example.com", "index.html")  # path 앞에 '/' 없어도 붙어야 함
    text = req.decode("utf-8")
    ok = (
        isinstance(req, bytes)
        and text.startswith("GET /index.html HTTP/1.1\r\n")
        and "\r\nHost: example.com\r\n" in text        # 헤더 이름은 'Host'
        and "\r\nConnection: close\r\n" in text         # 'Connection: close' (콜론 포함)
        and text.endswith("\r\n\r\n")                    # 헤더 끝은 빈 줄
    )
    if ok:
        print("✅ 요청 메시지 형식 정상!")
    else:
        print("❌ 요청 메시지 형식 오류. 생성된 값:")
        print(repr(req))
    print()

    # 테스트 8: parse_status_and_preview - 정상 응답 파싱
    print("--- [테스트 8: parse_status_and_preview 정상 응답] ---")
    body = "Hello, World! This is a test body."
    raw = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/plain\r\n"
        "Content-Length: 34\r\n"
        "\r\n"
        + body
    ).encode("utf-8")
    status, preview, error = parse_status_and_preview(raw, max_preview=10)
    if error is None and status == 200 and preview == body[:10]:
        print(f"✅ 파싱 성공! status={status}, preview={preview!r}")
    else:
        print(f"❌ 파싱 결과 오류: status={status}, preview={preview!r}, error={error}")
    print()

    # 테스트 9: parse_status_and_preview - 잘못된(비HTTP) 데이터
    print("--- [테스트 9: parse_status_and_preview 비정상 데이터] ---")
    status, preview, error = parse_status_and_preview(b"garbage without header boundary")
    if error is not None and status is None:
        print(f"✅ 에러 메시지 정상 반환: {error}")
    else:
        print(f"❌ 에러 처리 실패: status={status}, preview={preview!r}, error={error}")
    print()

    # 테스트 10: 실제 HTTP 서버 연동 (DNS -> TCP -> HTTP)
    host, port, path = "example.com", 80, "/"
    print(f"--- [테스트 10: 실제 서버 연동] http://{host}{path} ---")
    ips, dns_err = resolve(host)
    if dns_err:
        print(f"⚠️ DNS 실패로 건너뜀: {dns_err}")
    else:
        res = connect_with_fallback(ips, port, timeout=3.0, prefer="ipv4")
        if res.sock is None:
            print(f"⚠️ TCP 연결 실패로 건너뜀: {res.error}")
        else:
            try:
                raw = send_and_recv(res.sock, build_request(host, path), max_bytes=1_000_000)
                status, preview, error = parse_status_and_preview(raw, max_preview=80)
                if error is None and status is not None:
                    print(f"✅ 실제 응답 수신! status={status}")
                    print(f"   preview: {preview!r}")
                else:
                    print(f"❌ 응답 파싱 실패: status={status}, error={error}")
            except Exception as e:
                # build_request가 올바르지 않으면 서버가 응답하지 않아 recv가 timeout 날 수 있음
                print(f"⚠️ 요청/수신 중 예외 (build_request 형식 확인 필요): {e}")
            finally:
                res.sock.close()
    print()


def main():
    # 테스트 1: 정상적으로 연결되는 경우 (구글 DNS 서버)
    good_ip = "8.8.8.8"
    good_port = 53
    timeout_sec = 2.0

    print(f"--- [테스트 1: 연결 성공 케이스] {good_ip}:{good_port} ---")
    sock, ms, error = connect_one(good_ip, good_port, timeout_sec)

    if error is None:
        print("✅ 연결 성공!")
        print(f"소요 시간: {ms:.2f} ms")
        print(f"소켓 정보: {sock}")
        sock.close()  # 연결이 끝났으면 소켓을 닫아주는 것이 예의입니다.
    else:
        print(f"❌ 실패 (발생하면 안 됨): {error}")

    print("\n")

    # 테스트 2: 의도적으로 연결을 실패하게 만드는 경우 (없는 IP나 포트)
    bad_ip = "10.255.255.255"
    bad_port = 80

    print(f"--- [테스트 2: 연결 실패(Timeout) 케이스] {bad_ip}:{bad_port} ---")
    sock, ms, error = connect_one(bad_ip, bad_port, timeout_sec)

    if error is not None:
        print("✅ 의도된 연결 실패 (정상 동작)!")
        print(f"에러 메시지: {error}")
    else:
        print("❌ 성공함 (발생하면 안 됨!)")
        sock.close()

    print("\n")

    # 테스트 3: fallback 동작 확인 (앞의 IP는 실패, 뒤의 IP로 넘어가서 성공해야 함)
    fallback_ips = [bad_ip, good_ip]

    print(f"--- [테스트 3: Fallback 케이스] {fallback_ips}:{good_port} ---")
    res = connect_with_fallback(fallback_ips, good_port, timeout_sec)

    if res.error is None and res.ip == good_ip:
        print(f"✅ Fallback 성공! (첫 IP 실패 후 {res.ip}로 연결)")
        print(f"소요 시간: {res.connect_ms:.2f} ms")
        print(f"local: {res.local_addr} / peer: {res.peer_addr}")
        res.sock.close()
    elif res.error is None:
        print(f"❌ 연결은 됐지만 엉뚱한 IP: {res.ip} (기대값: {good_ip})")
        res.sock.close()
    else:
        print(f"❌ 실패 (발생하면 안 됨): {res.error}")

    print("\n")

    # 테스트 4: prefer 정책에 따른 순서 확인 (ipv6 우선 → v6 주소를 먼저 시도)
    mixed_ips = ["8.8.8.8", "2001:4860:4860::8888"]  # 구글 DNS v4 + v6

    print(f"--- [테스트 4: prefer='ipv6' 케이스] {mixed_ips}:{good_port} ---")
    res = connect_with_fallback(mixed_ips, good_port, timeout_sec, prefer="ipv6")

    if res.error is None:
        if ":" in res.ip:
            print(f"✅ IPv6 주소로 연결됨: {res.ip}")
        else:
            print(f"⚠️ IPv4로 연결됨: {res.ip}")
            print("   (IPv6 정렬이 틀렸거나, 이 네트워크에 IPv6가 없어서 fallback된 것일 수 있음)")
        res.sock.close()
    else:
        print(f"❌ 모두 실패: {res.error}")

    print("\n")

    # 테스트 5: 모든 IP가 실패하는 경우 (에러 메시지를 담아 반환해야 함)
    all_bad_ips = ["10.255.255.255", "10.255.255.254"]

    print(f"--- [테스트 5: 전체 실패 케이스] {all_bad_ips}:{bad_port} ---")
    res = connect_with_fallback(all_bad_ips, bad_port, timeout_sec)

    if res.error is not None and res.sock is None:
        print("✅ 의도된 전체 실패 (정상 동작)!")
        print(f"에러 메시지: {res.error}")
    else:
        print("❌ 성공하거나 에러가 비어 있음 (발생하면 안 됨!)")
        if res.sock:
            res.sock.close()

    print("\n")

    # 테스트 6: 빈 리스트를 넘기는 경우
    print("--- [테스트 6: 빈 리스트 케이스] ---")
    res = connect_with_fallback([], good_port, timeout_sec)

    if res.error == "No IPs to connect" and res.sock is None:
        print("✅ 빈 리스트 처리 정상!")
    else:
        print(f"❌ 예상과 다른 결과: error={res.error}")

    print("\n")

    # HTTP 로직 테스트
    test_http()

if __name__ == "__main__":
    main()