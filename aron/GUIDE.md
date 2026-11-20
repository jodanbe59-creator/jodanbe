# 아론 랜딩페이지 제작 가이드 (한국어)

> 스크롤로 전개되는 병의원 인테리어 스튜디오 랜딩페이지. 단일 HTML 파일에 **Three.js + GSAP**으로 만들었다(V1). 영상 버전(V2)은 **드리미나**로 이미지와 영상을 만들고 **ffmpeg**으로 후처리하는 구조까지 준비했다. 배포는 **Vercel**(폴더 끌어다 놓기).
>

**현재 상태:** V1 완성, 자료 반영 대기. V2는 보류.

---

## 1. 컨셉

병원과 상업 공간을 디자인하고 시공하는 인테리어 스튜디오 *ARON Design*의 원페이지 사이트. 첫 화면에서는 옅은 안개 속에 **ARON 로고**만 보인다. 스크롤하면 안개가 걷히며 밤의 도심이 드러나고, 평범한 상가 건물 4층의 **빈 콘크리트 층이 도면, 벽, 조명, 마감 순서로 지어진다**. 다 지어지면 아침이 밝으며 공간이 완성된다. 이어서 다섯 개의 패널이 인테리어 스튜디오의 일(공간, 디자인, 소재, 조명과 디테일, 시공)을 소개하고, 포트폴리오와 문의로 이어진다.

### 출발점: VERTANT 가이드를 응용

VERTANT의 "절벽 위에 지어지는 집"을 병원으로 바꾸면서 먼저 이 질문을 했다.

> 집을 의뢰하는 사람은 절벽 위의 멋진 집을 상상한다. 병원을 의뢰하는 원장님은 무엇을 상상할까?

정리한 답은 이렇다.
- 원장님의 출발점은 절벽이 아니라 **상가 건물의 빈 층**이다.
- 상상하는 장면은 건물 외관보다 **환자가 문을 열고 들어서는 순간**, 물 흐르듯 이어지는 동선, 간판에 불이 켜지는 순간이다.
- 집과 가장 다른 점은 **안심**에 대한 기대다. 큰 투자인 만큼 걱정 없이 완성되기를 바란다.

### 처음 준 브리프 (VERTANT와 같은 원문)

```
I want to build a single-page immersive 3D website using Three.js + GSAP,
single html file. Scroll-driven animation in the hero section that shows a
luxury mansion that gets built up on a cliff with scroll. 5 sections
triggered at specific scroll positions apart from the hero, each with
content panels (title, description). This is a builder website that shows
premium materials, craftsmanship, experience that build a one-of-a-kind
house. Smooth GSAP transitions. Theme: a luxury builder's landing page.
Performance: 60fps target.
```

### 아론 버전으로 바꾸며 준 방향 (요약)
- 업종: **병의원 인테리어 디자인 회사**. 예시 진료과로 피부과를 잡았다.
- 현실감: 로컬 의원부터 강남까지 다양한 원장님이 보시니 **비현실적이지 않게**. 초고층 빌딩 대신 평범한 상가 건물로.
- 말투: 개원 컨설팅 업체가 아니라 **인테리어 스튜디오의 결**로.
- 메뉴와 섹션 라벨은 **영어**, 본문은 한국어.
- 첫 화면: **로고가 가운데 뜨고, 스크롤하면 안개가 걷히며 건물이 보이게.**

---

## 2. 두 가지 버전

| 버전 | 히어로 방식 | 파일 | 상태 |
| --- | --- | --- | --- |
| **V1: 3D** | Three.js로 만든 클리닉 층이 스크롤에 따라 지어짐 | `v1-3d.html` | **완성 (메인)** |
| **V2: 영상** | AI 영상을 스크롤로 스크럽 | `v2-video.html` | 보류 (임시 영상 상태) |

VERTANT는 V1으로 콘셉트를 검증하고 V2를 배포했다. 아론은 반대로 **V1을 메인으로** 키웠다. 3D라서 메뉴, 패널, 카메라 장면을 수정할 때마다 영상을 다시 만들 필요가 없고, 비용도 들지 않기 때문이다.

---

## 3. V2용 영상 생성 계획 (드리미나)

순서는 VERTANT와 같다: **기준 이미지 → 6컷 스토리보드 → 빌드 영상 → 이어지는 영상 → 합본.** 이미지는 드리미나(Seedream 모델, 16:9, 최고 화질)로 만든다. 영상은 드리미나나 Higgsfield의 Seedance 2.0을 쓴다(Higgsfield 720p 기준 약 94크레딧).

핵심 아이디어는 **천장을 걷어낸 건축 모형 시점(단면도)**이다. 평면이 지어지는 과정이 한눈에 보인다. 빛은 VERTANT와 반대로 **밤의 공사 현장에서 개원일 아침**으로 흐른다. 병원은 하루를 마치는 곳이 아니라 시작하는 곳이기 때문이다.

### 3a. 기준 프레임 (완성된 모습)
```
Photorealistic architectural cutaway of a luxury private dermatology clinic
occupying one floor of a high-rise, ceiling removed, viewed from an elevated
3/4 angle like a premium architectural model. Curved warm-white plaster walls,
travertine floors, arched openings, champagne-gold metal details, soft cove
lighting. Zones: hotel-like reception lounge with sculptural desk, private
waiting pods, a quiet corridor, several serene treatment rooms with a single
treatment bed each. Floor-to-ceiling windows on one side showing a city
skyline in soft early-morning light. Calm, gallery-like, ultra-clean,
high-end interior photography. No text, no people.
```
> 평범한 실내 사진처럼 나오면 프롬프트 맨 앞에 `Dollhouse cutaway view, isometric, `를 붙인다.
> 지금은 "현실적인 상가 건물"로 방향이 바뀌었으니, 생성할 때 `high-rise`를 `mid-rise commercial building`으로 바꾸는 것을 검토한다.

### 3b. 6컷 스토리보드 (3a를 레퍼런스로)
```
A cinematic 6-panel storyboard (3 columns x 2 rows) of the SAME floor of the
SAME high-rise being transformed into the luxury dermatology clinic in the
reference image, seen as an architectural cutaway with the ceiling removed.
The camera performs ONE continuous move across the panels: starts high and
wide, slowly orbits right and lowers toward an elevated 3/4 angle while
zooming in. Lighting goes from night (work lights, city lights outside the
windows) to soft dawn to bright opening-day morning.
01 SHELL – empty raw concrete floor, columns, exposed ducts, night
02 PLAN – glowing floor-plan lines drawn across the concrete
03 WALLS – curved partition walls and arches rising along the lines
04 LIGHT – cove lighting and pendant fixtures appear, first dawn light
05 FINISHES – travertine floors, plaster, gold details, furniture in place
06 OPENING DAY – finished clinic glowing in morning sun, logo sign lit
No text, no people.
```

### 3c. 빌드 영상 (10초, 16:9, 스토리보드를 레퍼런스로, 오디오 없음)
```
One continuous cinematic 10-second shot, no cuts, following the six-stage
storyboard in order. An empty raw concrete floor of a high-rise transforms
itself into a luxury private dermatology clinic, seen as an architectural
cutaway with the ceiling removed: bare shell → glowing floor-plan lines →
curved walls and arches rise → cove lighting appears → travertine, plaster,
champagne-gold details and furniture settle in → finished clinic. The camera
performs ONE smooth continuous orbit to the right while lowering and zooming
in to an elevated 3/4 angle. Lighting transitions continuously from night
work lights → soft dawn → bright morning sun through the windows.
Photorealistic, ultra-smooth, premium architectural film. No people, no text.
```

### 3d. 이어지는 영상 (빌드 영상의 마지막 프레임을 시작 프레임으로)
```
One continuous cinematic shot beginning exactly on the provided image of the
finished luxury dermatology clinic in morning light. The camera smoothly
descends from the elevated cutaway view down to eye level at the glass
entrance, the doors slide open, and the camera glides forward through the
hotel-like reception lounge, along a softly lit curved corridor, and into a
serene private treatment room with a single treatment bed, warm diffused
light, and a city view through the window. Weightless, seamless, no cuts,
photorealistic. No people, no text.
```

> AI 영상은 글자를 깨뜨리므로 영상 속 간판은 추상 로고로만 두고, "ARON" 글자는 HTML로 얹는다.

---

## 4. 후처리 (ffmpeg): `build-hero.sh`

VERTANT의 ffmpeg 세 단계를 스크립트 하나로 묶었다.

```bash
# 첫 번째 클립의 마지막 프레임 추출 → 두 번째 클립의 시작 이미지로 사용
./build-hero.sh --last-frame build.mp4
```

```bash
# 두 클립을 이어 붙여 hero-sequence.mp4 + hero-poster.jpg 생성
./build-hero.sh build.mp4 inside.mp4
```

- 두 클립을 **24fps, 1280×720**으로 맞춘 뒤 이어 붙인다. 원본 크기가 달라도 된다.
- 오디오를 지우고 **올-인트라**(`-g 1`)로 인코딩한다. 어느 프레임이든 즉시 탐색할 수 있어 스크롤 스크럽이 부드럽다.
- `+faststart`로 메타데이터를 앞에 두고, 첫 프레임을 포스터로 뽑는다.

---

## 5. 페이지 & 애니메이션

### V1 (Three.js + GSAP ScrollTrigger, 단일 HTML, 외부 이미지 없음)

**스크롤 내러티브**
1. **안개 인트로:** 밝은 안개와 가운데 ARON 로고. 스크롤하면 CSS 안개가 걷히고, **3D 장면의 안개(FogExp2)도 밝은 안개색에서 밤 색으로 옅어지며** 건물이 실루엣부터 드러난다. 스크롤 아이콘을 누르면 바로 시공 장면으로 넘어간다.
2. **시공 (히어로 고정, 620vh):** GSAP 타임라인 하나(10단위)를 스크롤에 스크럽한다. PROCESS 01~06이 함께 진행된다.
   - 01 빈 공간: 밤, 작업등과 노출 덕트
   - 02 도면: 바닥에 평면선이 빛나며 그려짐 (선분 drawRange 애니메이션)
   - 03 벽체·아치: 벽이 바닥에서 솟아오름 (scale.y)
   - 04 조명: 간접조명 띠와 펜던트가 켜지고 새벽이 옴
   - 05 마감·가구: 트래버틴 바닥이 쓸리듯 깔리고, 회색 벽이 웜 화이트로 바뀌고, 가구가 놓이고, 덕트가 사라짐
   - 06 완성: 아침 햇살, 로고 사인 점등
3. **패널 5개:** 정해진 스크롤 위치에서 카메라가 각 장면으로 이동하고 패널이 등장한다.
   - SPACE: 위에서 본 평면, 방문객 동선이 금색 선으로 그려짐
   - DESIGN: 입구와 로고 사인
   - MATERIAL: 리셉션 데스크와 바닥
   - LIGHT & DETAIL: 라운지 펜던트와 창
   - CONSTRUCTION: 완성된 층 전체, 문의하기 버튼
4. **포트폴리오:** ALL / CLINIC / COMMERCIAL / HOSPITAL 필터. HOSPITAL에 경희온생한의원, 광명마디원정형외과, 다산에이아이정형외과.
5. **푸터:** INQUIRIES · LOCATION · FOLLOW.

**메뉴:** 왼쪽에 ARON 로고(안개가 걷히면 나타남), 가운데에 INTERIOR ▾ · CONTACT · FOLLOW. INTERIOR는 하위 분류(포트폴리오 필터)를 연다. 휴대폰에서는 로고와 겹치지 않게 메뉴를 오른쪽에 둔다.

**장면 구성**
- 클리닉 층: 36×18m 바닥판, 아치 개구부가 있는 벽(ExtrudeGeometry), 곡면 벽(열린 원기둥), 대기 포드, 시술실 4개, 상담실, 원장실, 라운지
- 건물: 5~6층 상가(석재 띠 + 띠창 텍스처), 주변은 2~8층 상가와 사무용 빌딩을 섞어 InstancedMesh로 배치, 바닥에 도로 텍스처
- 시간대: 밤 → 새벽 → 일출 → 아침, 하늘 셰이더와 태양 방향, 도시 창문 불빛이 함께 바뀜
- 텍스처: 콘크리트, 트래버틴, 창문, 도로를 모두 캔버스로 직접 그림

**성능 (60fps 목표)**
- 그림자 맵은 무언가 움직일 때만 다시 그린다 (`shadowMap.autoUpdate = false`)
- 기둥, 창틀, 주변 건물은 인스턴싱
- 픽셀 비율 상한 1.75(휴대폰 1.5), 프레임이 20ms를 넘으면 자동으로 낮춤
- 렌더 루프는 `gsap.ticker`에서 돌려 스크롤 트윈과 같은 프레임을 공유
- `prefers-reduced-motion` 존중

### V2 (GSAP만, 영상 스크럽)
- 서리 유리 와이프 → 빌드(영상 0~50%) → 패널(50~75%) → 실내 "들어오세요."(75~100%)
- 영상을 `fetch`로 통째로 받아 **blob URL**로 재생한다. range 요청을 지원하지 않는 서버에서도 스크럽이 된다.
- seek-chase 루프: 스크롤이 목표 시간을 정하고, 이전 탐색이 끝났을 때만 다음 탐색을 한다.

**타이포:** Cormorant Garamond(영문 제목, 로고) + Noto Serif KR(한글 제목) + Noto Sans KR(본문).
**색:** 웜 아이보리 #f6f1ea, 잉크 #2a2520, 샴페인 골드 #b08d57 / #d8bf93, 밤 #10131b. 로고의 베이지 사선(#bea286 부근)과 어울린다.

---

## 6. 배포 (Vercel, 폴더 끌어다 놓기)

1. 배포용 폴더를 만든다. `index.html`(= V1)과 `og.jpg`(카톡 미리보기 이미지)를 넣는다.
2. Vercel에서 **새 만들기 → 프로젝트**를 누르고, 폴더를 화면에 끌어다 놓은 뒤 **배포**를 누른다.
3. 나온 주소를 카톡으로 공유한다. 로그인 없이 누구나 열 수 있다.

> ⚠️ **프로젝트 이름에 한글은 안 된다.** "아론2" 대신 폴더 이름을 `aron2`로 했다.
> ⚠️ **토큰 방식은 쓰지 않았다.** Claude 앱에서 토큰 보안 입력 카드가 뜨지 않았기 때문이다. 끌어다 놓기가 가장 간단하다.
> Claude 아티팩트 링크도 "링크가 있는 모든 사람"으로 공유를 켜면 계정 없이 볼 수 있다. 공유 설정은 사용자가 직접 켜야 한다.

---

## 7. 함정 & 배운 점

**기획**
- **업종의 결을 지켜야 한다.** 처음에는 진료 상담, 인허가, 개원일 같은 *개원 컨설팅* 말투가 됐다. 인테리어 스튜디오는 공간, 디자인, 소재, 빛, 시공을 이야기해야 한다.
- **현실감이 신뢰를 만든다.** 초고층 빌딩 숲은 비현실적이라는 피드백을 받았다. 평범한 상가 건물과 2~8층 주변 건물로 바꿨다.
- **페이지 안 안내 문구는 방문자에게도 보인다.** "스크롤하여 시공 시작" 같은 제작자용 문구는 회사 소개 문장과 아이콘으로 바꿨다.
- **"화이트톤만 하는 곳"으로 보이지 않게.** 아론의 정체성은 색이 아니라 곡선, 간접조명의 선, 질감의 대비, 정돈된 디테일로 설명한다.
- **혼자 결정하지 않는다.** 위치나 문구는 후보를 먼저 보여 주고 확인받은 뒤 반영한다.

**기술**
- **테스트 환경의 느린 렌더링에 속지 말 것.** 그래픽카드 없는 환경에서는 프레임당 약 0.5초가 걸린다. GSAP의 lag smoothing 때문에 애니메이션이 슬로 모션처럼 보여서 버그로 착각하기 쉽다. 테스트할 때만 `gsap.ticker.lagSmoothing(0)`을 켠다.
- **스크롤 구간이 실제 스크롤 범위 안에 있는지 확인할 것.** V2 피날레 글자가 끝까지 나타나지 않았던 원인은, 등장 구간(70% 지점)이 섹션의 실제 스크롤 범위 밖에 있었기 때문이다.
- **호버로 여는 메뉴는 클릭과 충돌한다.** 마우스를 올려 열린 하위 메뉴가 이어진 클릭에 닫혔다. 호버로 연 직후의 클릭은 열린 상태를 유지하도록 했다.
- **가상 요소가 내용 위에 겹칠 수 있다.** 안개의 흰 덩어리(`::after`)가 로고 위에 그려져 오른쪽 글자가 흐려졌다. 내용에 `z-index`를 준다(로고 적용 때 수정 예정).
- **좁은 화면의 메뉴는 실제 폭으로 확인할 것.** 360px 휴대폰에서 "INTERIOR ▾"와 "CONTACT"가 붙어서 간격과 자간을 줄였다.
- **V2 임시 영상은 V1에서 녹화했다.** `#capture` 모드에서 카메라 경로를 직접 지정해 프레임을 뽑고, 4개를 병렬로 돌려 녹화 시간을 줄였다.

---

## 8. 에셋 & 파일 목록 (`aron/`)

| 파일 | 설명 |
| --- | --- |
| `v1-3d.html` | 메인 페이지 (Three.js 3D) |
| `v2-video.html` | 영상 스크럽 버전 (보류) |
| `hero-sequence.mp4`, `hero-poster.jpg` | V2 임시 영상과 포스터 (V1 녹화본) |
| `build-hero.sh` | 클립 합본·인코딩 스크립트 |
| `hub.html` | V1/V2 선택 첫 화면 |
| `assets/` | 로고 원본, 배경 제거본(어두운·밝은·ARON만), 파비콘 "A" |
| `NOTES.md` | 진행 메모, 결정 대기 항목, 요청 자료 |
| `GUIDE.md` | 이 문서 |

---

## 9. 사용 툴

**Claude Code**(기획·빌드·테스트) · **Three.js 0.160**(3D) · **GSAP 3.12 / ScrollTrigger**(애니메이션) · **드리미나**(V2 이미지·영상 예정) · **ffmpeg**(합본·인코딩) · **Playwright**(화면 확인·녹화) · **Vercel**(호스팅).
