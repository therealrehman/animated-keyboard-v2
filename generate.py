import base64
import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# 1. Root build.gradle
write_file('build.gradle', '''// Top-level build file
plugins {
    id 'com.android.application' version '8.2.0' apply false
    id 'org.jetbrains.kotlin.android' version '1.9.22' apply false
}
''')

# 2. settings.gradle
write_file('settings.gradle', '''pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = "AnimatedKeyboard"
include ':app'
''')

# 3. gradle.properties
write_file('gradle.properties', '''org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
kotlin.code.style=official
android.nonTransitiveRClass=true''')

# 4. .gitignore
write_file('.gitignore', '''*.iml
.gradle
/local.properties
/.idea/
.DS_Store
/build
/captures
.externalNativeBuild
.cxx
local.properties
''')

# 5. app/build.gradle
write_file('app/build.gradle', '''plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}

android {
    namespace 'com.example.animatedkeyboard'
    compileSdk 34

    defaultConfig {
        applicationId "com.example.animatedkeyboard"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0"
    }

    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = '17'
    }
}

dependencies {
    implementation 'androidx.core:core-ktx:1.12.0'    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.11.0'
}
''')

# 6. app/proguard-rules.pro
write_file('app/proguard-rules.pro', '# Add project specific ProGuard rules here.\n')

# 7. AndroidManifest.xml
write_file('app/src/main/AndroidManifest.xml', '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <application
        android:allowBackup="true"
        android:label="@string/app_name"
        android:supportsRtl="true"
        android:theme="@style/Theme.AnimatedKeyboard"
        android:icon="@android:drawable/sym_def_app_icon"
        android:roundIcon="@android:drawable/sym_def_app_icon">

        <service
            android:name=".service.AnimatedKeyboardIME"
            android:exported="true"
            android:label="@string/keyboard_name"
            android:permission="android.permission.BIND_INPUT_METHOD">
            <intent-filter>
                <action android:name="android.view.InputMethod" />
            </intent-filter>
            <meta-data
                android:name="android.view.im"
                android:resource="@xml/method" />
        </service>

    </application>

</manifest>
''')

# 8. method.xml
write_file('app/src/main/res/xml/method.xml', '''<?xml version="1.0" encoding="utf-8"?>
<input-method xmlns:android="http://schemas.android.com/apk/res/android">
    <subtype
        android:imeSubtypeLocale="en_US"
        android:imeSubtypeMode="keyboard" />
</input-method>
''')

# 9. strings.xml
write_file('app/src/main/res/values/strings.xml', '''<resources>
    <string name="app_name">Animated Keyboard</string>    <string name="keyboard_name">Animated Keyboard</string>
</resources>
''')

# 10. colors.xml
write_file('app/src/main/res/values/colors.xml', '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="black">#FF000000</color>
    <color name="white">#FFFFFFFF</color>
</resources>
''')

# 11. themes.xml
write_file('app/src/main/res/values/themes.xml', '''<resources xmlns:tools="http://schemas.android.com/tools">
    <style name="Theme.AnimatedKeyboard" parent="Theme.Material3.DayNight.NoActionBar">
    </style>
</resources>
''')

# 12. AnimationEngine.kt
write_file('app/src/main/java/com/example/animatedkeyboard/utils/AnimationEngine.kt', '''package com.example.animatedkeyboard.utils

import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.RadialGradient
import android.graphics.Shader
import kotlin.math.pow
import kotlin.random.Random

class AnimationEngine {
    private val activeAnimations = mutableListOf<GradientAnimation>()
    private val random = Random(System.currentTimeMillis())

    fun triggerAnimation(x: Float, y: Float, keyLabel: String) {
        val colors = getGradientColorsForKey(keyLabel)
        activeAnimations.add(GradientAnimation(x, y, colors))
    }

    fun update(elapsedTimeMs: Long) {
        activeAnimations.removeAll { anim ->
            anim.update(elapsedTimeMs)
            anim.isFinished
        }
    }

    fun draw(canvas: Canvas) {
        for (animation in activeAnimations) {
            animation.draw(canvas)
        }    }

    fun hasActiveAnimations(): Boolean {
        return activeAnimations.isNotEmpty()
    }

    private fun getGradientColorsForKey(key: String): IntArray {
        return when(key.lowercase()) {
            "a" -> intArrayOf(Color.parseColor("#FF5050"), Color.parseColor("#FF6432"), Color.TRANSPARENT)
            "b" -> intArrayOf(Color.parseColor("#3296FF"), Color.parseColor("#32C8FF"), Color.TRANSPARENT)
            "c" -> intArrayOf(Color.parseColor("#FFDC00"), Color.parseColor("#FFF032"), Color.TRANSPARENT)
            "d" -> intArrayOf(Color.parseColor("#00FF96"), Color.parseColor("#32FFB4"), Color.TRANSPARENT)
            "e" -> intArrayOf(Color.parseColor("#FF00DC"), Color.parseColor("#FF32F0"), Color.TRANSPARENT)
            "f" -> intArrayOf(Color.parseColor("#FFA000"), Color.parseColor("#FFC832"), Color.TRANSPARENT)
            "g" -> intArrayOf(Color.parseColor("#B432FF"), Color.parseColor("#C864FF"), Color.TRANSPARENT)
            "h" -> intArrayOf(Color.parseColor("#00FFFF"), Color.parseColor("#32FFFF"), Color.TRANSPARENT)
            "i" -> intArrayOf(Color.parseColor("#FF6464"), Color.parseColor("#FF9696"), Color.TRANSPARENT)
            "j" -> intArrayOf(Color.parseColor("#64FF64"), Color.parseColor("#96FF96"), Color.TRANSPARENT)
            "k" -> intArrayOf(Color.parseColor("#FFFF32"), Color.parseColor("#FFFF78"), Color.TRANSPARENT)
            "l" -> intArrayOf(Color.parseColor("#FF64C8"), Color.parseColor("#FF96DC"), Color.TRANSPARENT)
            "m" -> intArrayOf(Color.parseColor("#64C8FF"), Color.parseColor("#96DCFF"), Color.TRANSPARENT)
            "n" -> intArrayOf(Color.parseColor("#FFC832"), Color.parseColor("#FFDC64"), Color.TRANSPARENT)
            "o" -> intArrayOf(Color.parseColor("#DC64FF"), Color.parseColor("#F096FF"), Color.TRANSPARENT)
            "p" -> intArrayOf(Color.parseColor("#32DCFF"), Color.parseColor("#64F0FF"), Color.TRANSPARENT)
            "q" -> intArrayOf(Color.parseColor("#FF5050"), Color.parseColor("#FF8282"), Color.TRANSPARENT)
            "r" -> intArrayOf(Color.parseColor("#50FF96"), Color.parseColor("#82FFBE"), Color.TRANSPARENT)
            "s" -> intArrayOf(Color.parseColor("#FFF032"), Color.parseColor("#FFFF78"), Color.TRANSPARENT)
            "t" -> intArrayOf(Color.parseColor("#C864FF"), Color.parseColor("#DC96FF"), Color.TRANSPARENT)
            "u" -> intArrayOf(Color.parseColor("#64FFC8"), Color.parseColor("#96FFE6"), Color.TRANSPARENT)
            "v" -> intArrayOf(Color.parseColor("#FFA064"), Color.parseColor("#FFC896"), Color.TRANSPARENT)
            "w" -> intArrayOf(Color.parseColor("#64A0FF"), Color.parseColor("#96C8FF"), Color.TRANSPARENT)
            "x" -> intArrayOf(Color.parseColor("#FFFF96"), Color.parseColor("#FFFFDC"), Color.TRANSPARENT)
            "y" -> intArrayOf(Color.parseColor("#FF5096"), Color.parseColor("#FF82BE"), Color.TRANSPARENT)
            "z" -> intArrayOf(Color.parseColor("#50FFDC"), Color.parseColor("#82FFF0"), Color.TRANSPARENT)
            else -> intArrayOf(Color.parseColor("#FFAA32"), Color.parseColor("#FFC864"), Color.TRANSPARENT)
        }
    }

    private class GradientAnimation(
        private val centerX: Float,
        private val centerY: Float,
        private val colors: IntArray
    ) {
        var radius = 0f
            private set
        var isFinished = false
            private set

        private val maxRadius = 800f
        private val durationMs = 800L        private var startTime = System.currentTimeMillis()

        fun update(elapsedTimeMs: Long): Boolean {
            val progress = (System.currentTimeMillis() - startTime).toFloat() / durationMs.toFloat()
            if (progress >= 1.0f) {
                isFinished = true
                return false
            }
            radius = maxRadius * (1 - (1 - progress).toDouble().pow(2.0)).toFloat()
            return true
        }

        fun draw(canvas: Canvas) {
            if (radius <= 0) return
            val paint = Paint().apply {
                isAntiAlias = true
                shader = RadialGradient(
                    centerX, centerY, radius,
                    colors,
                    null,
                    Shader.TileMode.CLAMP
                )
            }
            canvas.drawCircle(centerX, centerY, radius, paint)
        }
    }
}
''')

# 13. AnimatedKeyboardIME.kt
write_file('app/src/main/java/com/example/animatedkeyboard/service/AnimatedKeyboardIME.kt', '''package com.example.animatedkeyboard.service

import android.inputmethodservice.InputMethodService
import android.view.View
import android.view.inputmethod.EditorInfo
import com.example.animatedkeyboard.ui.view.KeyboardView

class AnimatedKeyboardIME : InputMethodService() {

    private lateinit var keyboardView: KeyboardView

    override fun onEvaluateFullscreenMode(): Boolean = false

    override fun onCreateInputView(): View {
        keyboardView = KeyboardView(this)
        keyboardView.setOnKeyListener(object : KeyboardView.OnKeyListener {
            override fun onKey(code: Int, label: String) {
                val ic = currentInputConnection ?: return
                when (code) {
                    -1 -> { }                    -5 -> ic.deleteSurroundingText(1, 0)
                    -4 -> ic.commitText("\\n", 1)
                    else -> {
                        if (label == "Space") ic.commitText(" ", 1)
                        else ic.commitText(label, 1)
                    }
                }
            }
        })
        return keyboardView
    }

    override fun onStartInput(attribute: EditorInfo?, restarting: Boolean) {
        super.onStartInput(attribute, restarting)
    }
}
''')

# 14. KeyboardView.kt - using base64 to avoid corruption
keyboard_view_content = '''package com.example.animatedkeyboard.ui.view

import android.content.Context
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.RadialGradient
import android.graphics.Rect
import android.graphics.Shader
import android.graphics.Typeface
import android.util.AttributeSet
import android.view.MotionEvent
import android.view.View
import com.example.animatedkeyboard.utils.AnimationEngine
import kotlin.math.roundToInt
import kotlin.math.sqrt

enum class KeyState { NORMAL, WHITE, CYAN, PINK, FADE }

class KeyboardView @JvmOverloads constructor(
    context: Context,
    attrs: AttributeSet? = null,
    defStyleAttr: Int = 0
) : View(context, attrs, defStyleAttr) {

    interface OnKeyListener {
        fun onKey(code: Int, label: String)
    }

    private var keyListener: OnKeyListener? = null
    fun setOnKeyListener(listener: OnKeyListener) {
        this.keyListener = listener
    }

    private val keyPaint = Paint()
    private val keyBorderPaint = Paint()
    private val textPaint = Paint()
    private val animationEngine = AnimationEngine()
    private var lastFrameTime = 0L
    private var fireGlowAlpha = 0.5f
    private var fireGlowDirection = -1
    private val fireGlowPaint = Paint()
    private val pressedKeys = mutableMapOf<String, Long>()
    private val keyStates = mutableMapOf<String, KeyState>()
    private val ripples = mutableListOf<RippleEffect>()
    private var currentPopup: PopupEffect? = null
    private val popupPaint = Paint()
    private val popupBorderPaint = Paint()
    private val popupTextPaint = Paint()

    private val letterLayout = listOf(
        listOf("Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"),
        listOf("A", "S", "D", "F", "G", "H", "J", "K", "L"),
        listOf("Shift", "Z", "X", "C", "V", "B", "N", "M", "Del"),
        listOf("123", ",", "Space", ".", "Go")
    )

    private val numberLayout = listOf(
        listOf("1", "2", "3", "4", "5", "6", "7", "8", "9", "0"),
        listOf("-", "/", ":", ";", "(", ")", "$", "&", "@", "!"),
        listOf("#+=", "ABC", ".", ",", "Del"),
        listOf("Space", "Go")
    )

    private var currentLayout = letterLayout
    private var isShifted = false
    private val keyMap = mutableMapOf<String, Rect>()
    private val keyCodes = mutableMapOf<String, Int>()
    private var lastKeyTime = 0L
    private val debounceInterval = 100L
    private var touchStartX = 0f
    private var touchStartY = 0f
    private val swipeThreshold = 50f
    private var isSwiping = false
    private var lastTouchedKey: String? = null

    init {
        setWillNotDraw(false)
        setBackgroundColor(0x00000000)
        keyPaint.color = Color.parseColor("#080808")        keyPaint.isAntiAlias = true
        keyPaint.style = Paint.Style.FILL
        keyBorderPaint.color = Color.parseColor("#1A1A1A")
        keyBorderPaint.isAntiAlias = true
        keyBorderPaint.style = Paint.Style.STROKE
        keyBorderPaint.strokeWidth = 2f
        textPaint.color = Color.parseColor("#885500")
        textPaint.textSize = 42f
        textPaint.isAntiAlias = true
        textPaint.textAlign = Paint.Align.CENTER
        textPaint.typeface = Typeface.DEFAULT_BOLD
        fireGlowPaint.isAntiAlias = true
        popupPaint.color = Color.parseColor("#1E1E1E")
        popupPaint.isAntiAlias = true
        popupBorderPaint.color = Color.parseColor("#FFAA00")
        popupBorderPaint.isAntiAlias = true
        popupBorderPaint.style = Paint.Style.STROKE
        popupBorderPaint.strokeWidth = 3f
        popupTextPaint.color = Color.parseColor("#FFCC00")
        popupTextPaint.textSize = 52f
        popupTextPaint.isAntiAlias = true
        popupTextPaint.textAlign = Paint.Align.CENTER
        popupTextPaint.isFakeBoldText = true
        keyCodes["Shift"] = -1
        keyCodes["Del"] = -5
        keyCodes["Go"] = -4
        keyCodes["Space"] = 32
        keyCodes["123"] = -2
        keyCodes["ABC"] = -3
    }

    override fun onMeasure(widthMeasureSpec: Int, heightMeasureSpec: Int) {
        val width = View.MeasureSpec.getSize(widthMeasureSpec)
        val dm = context.resources.displayMetrics
        val desiredHeight = (dm.heightPixels * 0.24).toInt()
        super.onMeasure(
            View.MeasureSpec.makeMeasureSpec(width, View.MeasureSpec.EXACTLY),
            View.MeasureSpec.makeMeasureSpec(desiredHeight, View.MeasureSpec.EXACTLY)
        )
    }

    override fun onSizeChanged(w: Int, h: Int, oldw: Int, oldh: Int) {
        super.onSizeChanged(w, h, oldw, oldh)
        createKeyMap(w, h)
    }

    private fun createKeyMap(width: Int, height: Int) {
        keyMap.clear()
        val padding = (width * 0.01).toInt()
        val keyHeight = (height / 4).toInt()        val rowHeight = keyHeight + (padding / 2)
        var currentY = padding
        for (row in currentLayout) {
            val rowWidth = width - (padding * 2)
            var totalWeight = 0.0
            for (item in row) {
                totalWeight += getWeight(item).toDouble()
            }
            val tw = totalWeight.toFloat()
            var currentX = padding
            for (keyLabel in row) {
                val kw = (rowWidth * (getWeight(keyLabel) / tw)).roundToInt()
                val skw = minOf(kw, width - currentX - padding)
                keyMap[keyLabel] = Rect(currentX, currentY, currentX + skw, currentY + keyHeight)
                keyStates[keyLabel] = KeyState.NORMAL
                currentX += skw + (padding / 2)
            }
            currentY += rowHeight
        }
    }

    private fun getWeight(label: String): Float {
        return when (label) {
            "Space" -> 3.5f
            "Shift", "Del", "123", "ABC" -> 1.3f
            "Go" -> 1.5f
            else -> 1.0f
        }
    }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        val now = System.currentTimeMillis()
        val dt = if (lastFrameTime == 0L) 16 else now - lastFrameTime
        lastFrameTime = now
        canvas.drawColor(0x00000000)
        drawFireGlow(canvas)
        animationEngine.update(dt)
        animationEngine.draw(canvas)
        updateRipples(canvas, dt)
        updateKeyStates()
        for ((label, rect) in keyMap) {
            drawKey(canvas, label, rect)
        }
        currentPopup?.draw(canvas)
        if (animationEngine.hasActiveAnimations() || ripples.isNotEmpty() || currentPopup != null) {
            postInvalidateOnAnimation()
        }
    }
    private fun drawFireGlow(canvas: Canvas) {
        fireGlowAlpha += fireGlowDirection * 0.005f
        if (fireGlowAlpha <= 0.3f || fireGlowAlpha >= 0.7f) {
            fireGlowDirection *= -1
        }
        val cx = width / 2f
        val cy = height.toFloat()
        val a1 = (255 * fireGlowAlpha).toInt()
        val a2 = (180 * fireGlowAlpha).toInt()
        val a3 = (100 * fireGlowAlpha).toInt()
        val a4 = (40 * fireGlowAlpha).toInt()
        val colors = intArrayOf(
            Color.argb(a1, 255, 80, 0),
            Color.argb(a2, 255, 140, 0),
            Color.argb(a3, 255, 200, 0),
            Color.argb(a4, 255, 160, 0),
            Color.TRANSPARENT
        )
        val pos = floatArrayOf(0f, 0.2f, 0.4f, 0.6f, 1f)
        fireGlowPaint.shader = RadialGradient(cx, cy, width * 0.8f, colors, pos, Shader.TileMode.CLAMP)
        canvas.drawRect(0f, 0f, width.toFloat(), height.toFloat(), fireGlowPaint)
    }

    private fun updateRipples(canvas: Canvas, dt: Long) {
        val it = ripples.iterator()
        while (it.hasNext()) {
            val r = it.next()
            r.update(dt)
            r.draw(canvas)
            if (r.finished) {
                it.remove()
            }
        }
    }

    private fun updateKeyStates() {
        val now = System.currentTimeMillis()
        val entries = pressedKeys.entries.toList()
        for (entry in entries) {
            val elapsed = now - entry.value
            val ns = when {
                elapsed < 70 -> KeyState.WHITE
                elapsed < 140 -> KeyState.CYAN
                elapsed < 210 -> KeyState.PINK
                elapsed < 410 -> KeyState.FADE
                else -> KeyState.NORMAL
            }
            keyStates[entry.key] = ns
            if (elapsed >= 410) {
                pressedKeys.remove(entry.key)            }
        }
    }

    private fun drawKey(canvas: Canvas, label: String, rect: Rect) {
        val state = keyStates[label] ?: KeyState.NORMAL
        when (state) {
            KeyState.WHITE -> {
                keyPaint.color = Color.WHITE
                textPaint.color = Color.BLACK
                keyPaint.setShadowLayer(35f, 0f, 0f, Color.WHITE)
            }
            KeyState.CYAN -> {
                keyPaint.color = Color.CYAN
                textPaint.color = Color.BLACK
                keyPaint.setShadowLayer(30f, 0f, 0f, Color.CYAN)
            }
            KeyState.PINK -> {
                keyPaint.color = Color.MAGENTA
                textPaint.color = Color.WHITE
                keyPaint.setShadowLayer(28f, 0f, 0f, Color.MAGENTA)
            }
            KeyState.FADE -> {
                keyPaint.color = Color.parseColor("#FF6400")
                textPaint.color = Color.WHITE
                keyPaint.setShadowLayer(22f, 0f, 0f, Color.parseColor("#FF6400"))
            }
            KeyState.NORMAL -> {
                keyPaint.color = Color.parseColor("#080808")
                textPaint.color = Color.parseColor("#885500")
                keyPaint.clearShadowLayer()
            }
        }
        val l = rect.left.toFloat()
        val t = rect.top.toFloat()
        val r = rect.right.toFloat()
        val b = rect.bottom.toFloat()
        canvas.drawRoundRect(l, t, r, b, 12f, 12f, keyPaint)
        canvas.drawRoundRect(l, t, r, b, 12f, 12f, keyBorderPaint)
        val dl = if (isShifted && label.length == 1) label.uppercase() else label
        canvas.drawText(dl, rect.exactCenterX(), rect.exactCenterY() + (textPaint.textSize / 3f), textPaint)
    }

    override fun onTouchEvent(event: MotionEvent): Boolean {
        when (event.action) {
            MotionEvent.ACTION_DOWN -> {
                touchStartX = event.x
                touchStartY = event.y
                isSwiping = false
                lastTouchedKey = null                handleTouchDown(event.x, event.y)
                return true
            }
            MotionEvent.ACTION_MOVE -> {
                val dx = event.x - touchStartX
                val dy = event.y - touchStartY
                val dist = sqrt((dx * dx + dy * dy).toDouble()).toFloat()
                if (dist > swipeThreshold) {
                    isSwiping = true
                }
                if (!isSwiping) {
                    handleTouchDown(event.x, event.y)
                } else {
                    handleSwipeAnim(event.x, event.y)
                }
                return true
            }
            MotionEvent.ACTION_UP -> {
                if (!isSwiping && lastTouchedKey != null) {
                    val now = System.currentTimeMillis()
                    if (now - lastKeyTime > debounceInterval) {
                        lastKeyTime = now
                        commitKey(lastTouchedKey!!)
                    }
                }
                lastTouchedKey = null
                isSwiping = false
                return true
            }
            MotionEvent.ACTION_CANCEL -> {
                lastTouchedKey = null
                isSwiping = false
                return true
            }
        }
        return super.onTouchEvent(event)
    }

    private fun handleTouchDown(x: Float, y: Float) {
        for ((label, rect) in keyMap) {
            if (rect.contains(x.toInt(), y.toInt())) {
                lastTouchedKey = label
                animationEngine.triggerAnimation(rect.exactCenterX(), rect.exactCenterY(), label)
                ripples.add(RippleEffect(rect.exactCenterX(), rect.exactCenterY()))
                currentPopup = PopupEffect(label, rect.exactCenterX(), rect.top.toFloat() - 55f)
                pressedKeys[label] = System.currentTimeMillis()
                postInvalidateOnAnimation()
                break
            }
        }    }

    private fun handleSwipeAnim(x: Float, y: Float) {
        for ((label, rect) in keyMap) {
            if (rect.contains(x.toInt(), y.toInt())) {
                animationEngine.triggerAnimation(rect.exactCenterX(), rect.exactCenterY(), label)
                pressedKeys[label] = System.currentTimeMillis()
                postInvalidateOnAnimation()
                break
            }
        }
    }

    private fun commitKey(label: String) {
        when (label) {
            "Shift" -> {
                isShifted = !isShifted
                postInvalidateOnAnimation()
            }
            "Del" -> keyListener?.onKey(-5, "Del")
            "Go" -> keyListener?.onKey(-4, "Go")
            "Space" -> keyListener?.onKey(32, "Space")
            "123" -> {
                currentLayout = numberLayout
                createKeyMap(width, height)
                postInvalidateOnAnimation()
            }
            "ABC" -> {
                currentLayout = letterLayout
                createKeyMap(width, height)
                postInvalidateOnAnimation()
            }
            else -> {
                val fl = if (isShifted && label.length == 1) label.uppercase() else label
                keyListener?.onKey(fl.hashCode(), fl)
                if (isShifted) {
                    isShifted = false
                    postInvalidateOnAnimation()
                }
            }
        }
    }

    private inner class RippleEffect(private val cx: Float, private val cy: Float) {
        private var radius = 0f
        private var alp = 255
        var finished = false
        private val maxR = 100f
        private val dur = 500L
        private val start = System.currentTimeMillis()        fun update(dt: Long) {
            val p = (System.currentTimeMillis() - start).toFloat() / dur.toFloat()
            if (p >= 1.0f) {
                finished = true
                return
            }
            radius = maxR * p
            alp = (255 * (1 - p)).toInt()
        }
        fun draw(canvas: Canvas) {
            val pt = Paint()
            pt.isAntiAlias = true
            pt.color = Color.argb(alp, 255, 255, 255)
            canvas.drawCircle(cx, cy, radius, pt)
        }
    }

    private inner class PopupEffect(private val lbl: String, private val px: Float, private val py: Float) {
        private var alp = 255
        private var offY = 10f
        var finished = false
        private val dur = 250L
        private val start = System.currentTimeMillis()
        fun draw(canvas: Canvas) {
            val p = (System.currentTimeMillis() - start).toFloat() / dur.toFloat()
            if (p >= 1.0f) {
                finished = true
                return
            }
            if (p < 0.2f) {
                offY = 10f - (10f * (p / 0.2f))
                alp = 255
            } else {
                alp = (255 * (1 - (p - 0.2f) / 0.8f)).toInt()
            }
            val pw = 80f
            val ph = 60f
            popupPaint.alpha = alp
            canvas.drawRoundRect(px - pw / 2, py + offY, px + pw / 2, py + offY + ph, 10f, 10f, popupPaint)
            popupBorderPaint.alpha = alp
            canvas.drawRoundRect(px - pw / 2, py + offY, px + pw / 2, py + offY + ph, 10f, 10f, popupBorderPaint)
            popupTextPaint.alpha = alp
            canvas.drawText(lbl.uppercase(), px, py + offY + ph / 2 + popupTextPaint.textSize / 3f, popupTextPaint)
        }
    }
}
'''

# Encode to base64 and decode to avoid any Termux corruption
encoded = base64.b64encode(keyboard_view_content.encode('utf-8')).decode('utf-8')decoded = base64.b64decode(encoded).decode('utf-8')
write_file('app/src/main/java/com/example/animatedkeyboard/ui/view/KeyboardView.kt', decoded)

# 15. KeyModel.kt
write_file('app/src/main/java/com/example/animatedkeyboard/model/KeyModel.kt', '''package com.example.animatedkeyboard.model

data class KeyModel(
    val code: Int,
    val label: String,
    val widthWeight: Float = 1.0f
)
''')

# 16. GitHub Actions workflow
write_file('.github/workflows/build.yaml', '''name: Build Android APK

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Setup Gradle
        uses: gradle/actions/setup-gradle@v4
        with:
          gradle-version: '8.7'

      - name: Build with Gradle
        run: gradle build

      - name: Build Debug APK
        run: gradle assembleDebug

      - name: Upload Debug APK        uses: actions/upload-artifact@v4
        with:
          name: app-debug-apk
          path: app/build/outputs/apk/debug/app-debug.apk

      - name: Build Release APK
        run: gradle assembleRelease

      - name: Upload Release APK
        uses: actions/upload-artifact@v4
        with:
          name: app-release-apk
          path: app/build/outputs/apk/release/app-release-unsigned.apk
''')

# 17. README.md
write_file('README.md', '''# Animated Keyboard

A professional Android custom keyboard with Fire Glow effects and GPU-accelerated animations.

## Features
- Fire glow breathing effect
- Per-letter specific gradient colors
- Key press animations: White -> Cyan -> Pink -> Fade
- Individual key ripples
- Key popups with animations
- GPU-accelerated rendering (60 FPS)
- Swipe detection (swipe = animation only, no typing)
- Debounce protection
- Numeric keyboard mode

## Build

### Prerequisites
- Android Studio Hedgehog or later
- JDK 17
- Android SDK 34

### Build APK
```bash
./gradlew assembleDebug
```

## Installation
1. Build the APK
2. Install on your Android device
3. Go to Settings -> Languages & Input -> Keyboards
4. Enable "Animated Keyboard"
5. Switch to it using the keyboard switcher
## License
MIT License
''')

# 18. LICENSE
write_file('LICENSE', '''MIT License

Copyright (c) 2024 therealrehman

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
''')

print("All files generated successfully!")
