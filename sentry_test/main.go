package main

import (
	"log"
	"net/http"
	"os"
	"time"

	"github.com/getsentry/sentry-go"
	sentrygin "github.com/getsentry/sentry-go/gin"
	"github.com/gin-gonic/gin"
)

func main() {
	if err := sentry.Init(sentry.ClientOptions{
		Dsn:              os.Getenv("SENTRY_DSN"),
		EnableTracing:    true,
		TracesSampleRate: 1.0,
	}); err != nil {
		log.Fatalf("Sentry initialization failed: %v\n", err)
	}

	r := gin.Default()
	r.Use(sentrygin.New(sentrygin.Options{}))

	r.GET("/", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"message": "pong",
		})
	})

	r.GET("/delay", func(c *gin.Context) {
		time.Sleep(time.Second * 2)
		c.JSON(http.StatusOK, gin.H{
			"message": "delay",
		})
	})

	r.GET("/error", func(c *gin.Context) {
		defer sentry.Recover()
		panic("Error Test")
	})

	r.Run() // listen and serve on 0.0.0.0:8080 (for windows "localhost:8080")
}
