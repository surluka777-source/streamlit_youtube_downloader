import streamlit as st
import yt_dlp
import os
from pathlib import Path

st.title("🚀 서버형 유튜브 다운로더")

url = st.text_input("다운로드할 유튜브 링크를 입력하세요:")

if st.button("영상 준비하기"):
    if url:
        with st.spinner("서버에서 영상을 처리 중입니다... (고화질일수록 오래 걸립니다)"):
            # 서버 내 임시 저장 위치
            save_dir = Path("downloads")
            save_dir.mkdir(exist_ok=True)
            
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
                'outtmpl': str(save_dir / '%(title)s.%(ext)s'),
                # 추가: 유튜브 추출기 인자 설정 (안드로이드 클라이언트 사용)
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android', 'ios'],
                    }
                },
                'quiet': True,
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    file_path = ydl.prepare_filename(info)

                # 준비된 파일을 사용자에게 전송
                with open(file_path, "rb") as f:
                    btn = st.download_button(
                        label="내 컴퓨터로 저장하기",
                        data=f,
                        file_name=os.path.basename(file_path),
                        mime="video/mp4"
                    )
                st.success("영상이 준비되었습니다!")
                
                # (선택) 서버 용량 관리를 위해 파일 삭제 로직을 추가할 수도 있습니다.
            except Exception as e:
                st.error(f"오류 발생: {e}")
    else:

        st.warning("링크를 입력해주세요.")
